using Microsoft.EntityFrameworkCore;
// Tells the EF core that the models should be database tables
namespace FxDataIngestor
{
    // Create class that inherits from the Dbcontext
    public class FxDbContext : DbContext
    {
        public DbSet<Instrument> Instruments {get; set;}
        public DbSet<Price> Prices {get; set;}

        // Override the configuration to tell the Dbcontext how to connect to the DB
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            // Choose which DB to use
            optionsBuilder.UseSqlite("Data Source=Fx_data.db");
        }

        // Override the primary key for prices so it is a composite key instead
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Tell EF-core what are the keys
            modelBuilder.Entity<Price>().HasKey(p => new{p.InstrumentId,p.Timeframe, p.BarTime});
        }

    }

}

