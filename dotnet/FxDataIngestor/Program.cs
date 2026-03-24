using FxDataIngestor;

var client = new FrankfurterClient();
var results = await client.GetLatestData("USD", "GBP");
Console.WriteLine(results);

var builder = Host.CreateApplicationBuilder(args);
builder.Services.AddHostedService<Worker>();

var host = builder.Build();
host.Run();


