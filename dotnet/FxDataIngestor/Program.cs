using FxDataIngestor;

var builder = Host.CreateApplicationBuilder(args);
builder.Services.AddSingleton<FrankfurterClient>();
builder.Services.AddSingleton<FxDbContext>();
builder.Services.AddSingleton<PriceIngestionService>();
builder.Services.AddHostedService<Worker>();


var host = builder.Build();
host.Run();


