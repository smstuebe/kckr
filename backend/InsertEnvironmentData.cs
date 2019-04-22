using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Microsoft.WindowsAzure.Storage.Table;

namespace Kckr.Functions
{
    public class EnvironmentDataDto : DeviceDto
    {
        public bool Occupied { get; set; }
        public double Temperature { get; set; }
        public double Humidity { get; set; }
    }

    public class EnvironmentDataEntity : ReverseOrderedDeviceEntity
    {
        public bool Occupied { get; set; }
        public double Temperature { get; set; }
        public double Humidity { get; set; }

        public EnvironmentDataEntity(EnvironmentDataDto dto) : base(dto)
        {
            Occupied = dto.Occupied;
            Temperature = dto.Temperature;
            Humidity = dto.Humidity;
        }
    }

    public static class InsertEnvironmentData
    {
        [FunctionName("InsertEnvironmentData")]
        [return: Table("environment")]
        public static async Task<EnvironmentDataEntity> Run(
            [HttpTrigger(AuthorizationLevel.Function, "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            var json = await req.ReadAsStringAsync();
            var envData = JsonConvert.DeserializeObject<EnvironmentDataDto>(json);

            var occupied = envData.Occupied ? "occupied" : "free";
            log.LogInformation($"New Environment Data for {envData.Location}: {occupied} {envData.Temperature:F2}°C {envData.Humidity:F2}%");

            return new EnvironmentDataEntity(envData);
        }
    }
}
