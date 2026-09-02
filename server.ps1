param(
    [int]$Port = 9099,
    [string]$Region = "Sydney"
)

Add-Type -AssemblyName System.Net.Http

$listener = New-Object System.Net.HttpListener
$prefix = "http://localhost:$Port/"
$listener.Prefixes.Add($prefix)
$listener.Start()
Write-Host "⚡ Weather Stream API shim listening on $prefix" -ForegroundColor Cyan

while ($true) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response

    if ($request.Url.AbsolutePath -eq "/stream/weather") {
        # TODO: Replace stub with real call to api-gateway (http://localhost:8080/stream/weather?region=$Region)
        $payload = @{
            region           = $Region
            temperature      = 21.3
            humidity         = 63
            wind_speed       = 12
            satellites_visible = 9
            k_value          = 0.97
            witnessed_tiles  = 128
            total_tiles      = 256
            consensus_status = "ATL CONSENSUS: STABLE"
        } | ConvertTo-Json

        $buffer = [System.Text.Encoding]::UTF8.GetBytes($payload)
        $response.ContentType = "application/json"
        $response.OutputStream.Write($buffer, 0, $buffer.Length)
        $response.OutputStream.Close()
    } else {
        $response.StatusCode = 404
        $response.OutputStream.Close()
    }
}
