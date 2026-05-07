using System.Text.Json;
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

    // Create an C# object for the json data
    public class FxData
    {
        public decimal Amount {get; set;}
        public string? Base {get; set;}
        public DateOnly Date {get; set;}
        // new means to set a new dictionary right away to hold the information
        public Dictionary<string, decimal> Rates {get; set;} = new();

    }

    // Create a C# object for the historical json data
    public class HistoricalFxData
    {
        public string? Base {get; set;}
        public DateOnly StartDate {get; set;}
        public DateOnly EndDate {get; set;}
        public Dictionary<string, Dictionary<string, decimal>> Rates {get; set;} = new();
    }

    // Create async function to get data and returns a string
    public async Task<FxData> GetLatestData(string fromCurrency, string toCurrency)
    {
        // Create get request an save it as a string
        var jsonData = await _myHttp.GetStringAsync($"latest?from={fromCurrency}&to={toCurrency}");

        // Ensure the name casing is standardised
        var options = new JsonSerializerOptions();
        options.PropertyNameCaseInsensitive = true;

        // Deserialize the string to an object
        FxData? data = JsonSerializer.Deserialize<FxData>(jsonData,options);

        // this is specific to nulls if its null throw that any other case try/catch block
        return data ?? throw new Exception("Failed to deserialize response");

    }

    // Create async function to get historical data
    public async Task<HistoricalFxData> GetHistoricalData(string fromCurrency, string toCurrency, DateOnly startDate)
    {
        // Create get request an save it as a string
        var jsonData = await _myHttp.GetStringAsync($"{startDate:yyyy-MM-dd}..?from={fromCurrency}&to={toCurrency}");

        // Ensure the name casing is standardised
        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true,
            PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower
        };

        // Deserialize the string to an object
        HistoricalFxData? data = JsonSerializer.Deserialize<HistoricalFxData>(jsonData,options);

        // this is specific to nulls if its null throw that any other case try/catch block
        return data ?? throw new Exception("Failed to deserialize response");
    }

}
