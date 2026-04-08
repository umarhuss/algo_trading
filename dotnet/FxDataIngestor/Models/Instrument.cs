using System.ComponentModel.DataAnnotations; // Needed for [Required]
using Microsoft.EntityFrameworkCore;         // Needed for [Index]

namespace FxDataIngestor
{
  [Index(nameof(Symbol), IsUnique = true)] // Makes symbol UNIQUE in SQL
  public class Instrument
  {
    public int Id { get; set; } // EF core should make this primary key automatically and auto increment.

    [Required]
    public string Symbol { get; set; } = string.Empty;

    [Required]
    public string Base { get; set; } = string.Empty;

    [Required]
    public string Quote { get; set; } = string.Empty;

    [Required]
    public string Type { get; set; } = string.Empty;


  }
}
