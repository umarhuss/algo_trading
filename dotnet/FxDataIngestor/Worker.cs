namespace FxDataIngestor;

public class Worker(ILogger<Worker> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            if (logger.IsEnabled(LogLevel.Information))
            {
                logger.LogInformation("Worker running at: {time}", DateTimeOffset.Now);
            }
            await Task.Delay(TimeSpan.FromSeconds(10), stoppingToken);
        }
    }

    private static DateTime ComputeNextRun()
    {
        // parameter version
        DateTime now = DateTime.UtcNow;

        return ComputeNextRun(now);
    }
    private static DateTime ComputeNextRun(DateTime now)
    {
        // Calculate the time interval for runs
        TimeSpan interval = new TimeSpan(15,05,00);
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
        while(nextRun.DayOfWeek == DayOfWeek.Saturday || nextRun.DayOfWeek == DayOfWeek.Sunday)
        {
            nextRun = nextRun.AddDays(1);
        }

        // Return to be used in the delay
        return nextRun;

    }


}



