using System.ComponentModel.DataAnnotations; // Needed for [Required]


namespace FxDataIngestor
{
    public class Price
    {
      public int InstrumentId { get; set; }

      [Required]
      public string Timeframe { get; set; } = string.Empty;

      public DateTime BarTime { get; set; }

      public decimal Close {get; set;}

      public Instrument? Instrument { get; set; }

    }
}
