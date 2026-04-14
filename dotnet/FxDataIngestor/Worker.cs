namespace FxDataIngestor;

public class Worker(ILogger<Worker> logger, PriceIngestionService ingestionService) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
            while (!stoppingToken.IsCancellationRequested)
            {

            // Create the time variables
            DateTime now = DateTime.UtcNow;
            DateTime nextRun = ComputeNextRun(now);
            TimeSpan delay = nextRun - now;

            // Ensure there is logging to the console so i know what is happening
            if (logger.IsEnabled(LogLevel.Information))
            {
                logger.LogInformation("Current Time: {time}", now);
                logger.LogInformation("Next run is: {time}", nextRun);
                logger.LogInformation("Current delay is: {time}", delay);
            }

            // Clamp the delay so if its ever negative the time span is changed to 0 so it executes right away
            if (delay < TimeSpan.Zero)
            {
                delay = TimeSpan.Zero;
            }

            // Call the task
            await Task.Delay(delay, stoppingToken);

             try
            {
                // While the task is happening log what is taking place
                logger.LogInformation("Ingestion of Data is in progress ....");
                // For now hardcode this later read from json settings more flexible
                await ingestionService.IngestPriceAsync("USD","GBP");
                logger.LogInformation("Ingestion completed");
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Ingestion failed");
            }


        }
    }

    protected

    private static DateTime ComputeNextRun()
    {
        // parameter version
        DateTime now = DateTime.UtcNow;

        return ComputeNextRun(now);
    }
    private static DateTime ComputeNextRun(DateTime now)
    {
        // Calculate the time interval for runs
        TimeSpan interval = new TimeSpan(15, 05, 00);
        // Calculate the current day
        DateTime todayTarget = now.Date + interval;
        // Variable for the next day
        DateTime nextRun;

        // Check if current time is <= that the target
        if (now <= todayTarget)
        {
            nextRun = todayTarget;
        }
        // If not go to the next day
        else
        {
            nextRun = todayTarget.AddDays(1);
        }

        // While the nextrun is a weekend go to the next day
        while (nextRun.DayOfWeek == DayOfWeek.Saturday || nextRun.DayOfWeek == DayOfWeek.Sunday)
        {
            nextRun = nextRun.AddDays(1);
        }

        // Return to be used in the delay
        return nextRun;

    }


}



