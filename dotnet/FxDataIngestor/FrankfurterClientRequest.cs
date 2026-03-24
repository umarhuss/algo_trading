// HttpClient lifecycle management best practices:
// https://learn.microsoft.com/dotnet/fundamentals/networking/http/httpclient-guidelines#recommended-use

namespace FxDataIngestor;

public class FrankfurterClient
{
    // declare a private HttpClient field here
    private readonly HttpClient _myHttp;

    // write a constructor that creates the HttpClient
    public FrankfurterClient()
    {
        _myHttp = new HttpClient();

        _myHttp.BaseAddress = new Uri("https://api.frankfurter.dev/v1/");
    }

    // Create async function to get data and returns a string
    public async Task<string> GetLatestData(string fromCurrency, string toCurrency)
    {
        // Create get request an save it as a string
        return await _myHttp.GetStringAsync($"latest?from={fromCurrency}&to={toCurrency}");
    }

}
