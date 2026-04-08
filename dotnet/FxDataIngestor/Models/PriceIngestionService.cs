using Microsoft.EntityFrameworkCore;

namespace FxDataIngestor;

public class PriceIngestionService
{
    // dependency injection
    private readonly FrankfurterClient _client;
    private readonly FxDbContext _context;

    public PriceIngestionService(FrankfurterClient client, FxDbContext context)
    {
        _client = client;
        _context = context;
    }

    // Create function to call the api and the db
    public async Task IngestPriceAsync(string fromCurrency, string toCurrency)
    {
        // Get the latest data
        var currFxData = await _client.GetLatestData(fromCurrency, toCurrency);
        // Get the symbol to check in database
        var currSymbol = $"{fromCurrency}/{toCurrency}";
        // Check the database to see if instrument is already there based on symbol
        var symbolCheck = await _context.Instruments.FirstOrDefaultAsync(i => i.Symbol== currSymbol);

        // variable to hold the id
        int instrumentId;
        // The symbol check will either be null or the full instrument row
        if (symbolCheck == null)
        {
            // Create a new instrument object
            var newInstrument = new Instrument
            {
                Symbol = currSymbol,
                Base = fromCurrency,
                Quote = toCurrency,
                Type = "Forex"

            };

            // Insert the instrument into the DB table
            _context.Instruments.Add(newInstrument);
            // commit the changes to the DB
            await _context.SaveChangesAsync();
            // Set the instrument variable to
            instrumentId = newInstrument.Id;
        }
        else
        {
            instrumentId = symbolCheck.Id;

        }
        //
         var newPrice = new Price
            {
                InstrumentId = instrumentId,
                Timeframe = "1D",
                BarTime = currFxData.Date,
                Close = currFxData.Rates[toCurrency],
            };

            _context.Prices.Add(newPrice);
            await _context.SaveChangesAsync();
    }
}
