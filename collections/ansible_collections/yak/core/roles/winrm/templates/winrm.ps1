# Copyright: (c) 2022, dbi services
# This file is part of YaK core.
# Yak core is free software distributed without any warranty under the terms of the GNU General Public License v3 as published by the Free Software Foundation, https://www.gnu.org/licenses/gpl-3.0.txt

{% if script_type == 'aws' %}
<powershell>
{% endif %}
{% if script_type == 'oci' %}
#ps1_sysnative
{% endif %}
# -----------------------------------------------------------------------
# Execution policy
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope LocalMachine -Force -ErrorAction Ignore
$ErrorActionPreference = 'stop'
$VerbosePreference = 'Continue'

# Functions
function Get-RandomCharacters($length, $characters) {
    $random = 1..$length | ForEach-Object { Get-Random -Maximum $characters.length }
    $private:ofs=""
    return [String]$characters[$random]
}
## https://www.powershellgallery.com/packages/Convert/0.2.0.5/Content/Public%5CConvertFrom-StringToByteArray.ps1
function ConvertFrom-StringToByteArray
{
    [CmdletBinding(HelpUri = 'http://convert.readthedocs.io/en/latest/functions/ConvertFrom-StringToByteArray/')]
    param
    (
        [Parameter(
            Mandatory = $true,
            ValueFromPipeline = $true,
            ValueFromPipelineByPropertyName = $true)]
        [ValidateNotNullOrEmpty()]
        [String[]]
        $String,

        [ValidateSet('ASCII', 'BigEndianUnicode', 'Default', 'Unicode', 'UTF32', 'UTF7', 'UTF8')]
        [String]
        $Encoding = 'UTF8'
    )

    begin
    {
        $userErrorActionPreference = $ErrorActionPreference
    }

    process
    {
        foreach ($s in $String)
        {
            # Creating a generic list to ensure an array of string being handed in
            # outputs an array of Byte arrays, rather than a single array with both
            # Byte arrays merged.
            $byteArrayObject = [System.Collections.Generic.List[Byte[]]]::new()
            try
            {
                $byteArray = [System.Text.Encoding]::$Encoding.GetBytes($s)
                $null = $byteArrayObject.Add($byteArray)
                $byteArrayObject
            }
            catch
            {
                Write-Error -ErrorRecord $_ -ErrorAction $userErrorActionPreference
            }
        }
    }
}

# Variables
$username = '{{ winrm_user }}'
$password = '{{ winrm_user_password }}'
$certificat_string = '{{ lookup('file', winrm_cert_pem_path) }}'
$certificat_bytes = ConvertFrom-StringToByteArray -String $certificat_string

# -----------------------------------------------------------------------
# Create the {{ winrm_user }} user
# -----------------------------------------------------------------------
$secure_string_password  = ConvertTo-SecureString "$password" -AsPlainText -Force
try { Get-LocalUser $username }
catch [Microsoft.PowerShell.Commands.UserNotFoundException] {
    New-LocalUser $username -Password $secure_string_password -FullName "$username" -Description "Account for Ansible automation"
}
try {
    Add-LocalGroupMember -Group "Administrators" -Member "$username"
} catch [Microsoft.PowerShell.Commands.MemberExistsException] {
    Write-Verbose "User '$username' already in group 'Administrators'. Keep going..."
}

# -----------------------------------------------------------------------
# Configure WinRM
# -----------------------------------------------------------------------
# Remove any existing Windows Management listeners
Remove-Item -Path WSMan:\Localhost\listener\listener* -Recurse

# Create self-signed cert for encrypted WinRM on port 5986
$Cert = New-SelfSignedCertificate -CertstoreLocation Cert:\LocalMachine\My -DnsName "packer-ami-builder"
New-Item -Path WSMan:\LocalHost\Listener -Transport HTTPS -Address * -CertificateThumbPrint $Cert.Thumbprint -Force

# Configure WinRM
cmd.exe /c winrm quickconfig -q
cmd.exe /c winrm set "winrm/config" '@{MaxTimeoutms="1800000"}'
cmd.exe /c winrm set "winrm/config/winrs" '@{MaxMemoryPerShellMB="1024"}'
cmd.exe /c winrm set "winrm/config/service" '@{AllowUnencrypted="false"}'
cmd.exe /c winrm set "winrm/config/client" '@{AllowUnencrypted="false"}'
cmd.exe /c winrm set "winrm/config/service/auth" '@{Basic="true"}'
cmd.exe /c winrm set "winrm/config/client/auth" '@{Basic="true"}'
cmd.exe /c winrm set "winrm/config/service/auth" '@{CredSSP="true"}'
cmd.exe /c winrm set "winrm/config/listener?Address=*+Transport=HTTPS" "@{Port=`"5986`";Hostname=`"packer-ami-builder`";CertificateThumbprint=`"$($Cert.Thumbprint)`"}"
cmd.exe /c netsh advfirewall firewall add rule name="WinRM-SSL (5986)" dir=in action=allow protocol=TCP localport=5986
cmd.exe /c net stop winrm
cmd.exe /c sc config winrm start= auto
cmd.exe /c net start winrm

# -----------------------------------------------------------------------
# Authorize certificat
# Ref. https://docs.ansible.com/ansible/latest/user_guide/windows_winrm.html
# -----------------------------------------------------------------------
Set-Item -Path WSMan:\localhost\Service\Auth\Certificate -Value $true

# -----------------------------------------------------------------------
# Import a Certificate to the Certificate Store
# Ref. https://docs.ansible.com/ansible/latest/user_guide/windows_winrm.html
# -----------------------------------------------------------------------
# Import the issuing certificate
$cert = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Certificate2
$cert.Import($certificat_bytes)

$store_name = [System.Security.Cryptography.X509Certificates.StoreName]::Root
$store_location = [System.Security.Cryptography.X509Certificates.StoreLocation]::LocalMachine
$store = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Store -ArgumentList $store_name, $store_location
$store.Open("MaxAllowed")
$store.Add($cert)
$store.Close()

# Import the client certificate public key
$cert = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Certificate2
$cert.Import($certificat_bytes)

$store_name = [System.Security.Cryptography.X509Certificates.StoreName]::TrustedPeople
$store_location = [System.Security.Cryptography.X509Certificates.StoreLocation]::LocalMachine
$store = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Store -ArgumentList $store_name, $store_location
$store.Open("MaxAllowed")
$store.Add($cert)
$store.Close()

# Mapping a Certificate to an Account
$credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $username, $secure_string_password
$thumbprint = (Get-ChildItem -Path cert:\LocalMachine\root | Where-Object { $_.Subject -eq "CN=$username" }).Thumbprint

New-Item -Path WSMan:\localhost\ClientCertificate `
    -Subject "$username@localhost" `
    -URI * `
    -Issuer $thumbprint `
    -Credential $credential `
    -Force

# -----------------------------------------------------------------------
{% if script_type == 'aws' %}</powershell>{% endif %}
