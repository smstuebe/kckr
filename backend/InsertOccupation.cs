using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace Kckr.Functions
{
    public class OccupationDto : DeviceDto
    {
        public bool Occupied { get; set; }
    }

    public class OccupationEntity : ReverseOrderedDeviceEntity
    {
        public bool Occupied { get; set; }

        public OccupationEntity(OccupationDto dto) : base(dto)
        {
            Occupied = dto.Occupied;
        }
    }

    public static class InsertOccupation
    {
        [FunctionName("InsertOccupation")]
        [return: Table("occupation")]
        public static async Task<OccupationEntity> Run(
            [HttpTrigger(AuthorizationLevel.Function, "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            var json = await req.ReadAsStringAsync();
            var occupation = JsonConvert.DeserializeObject<OccupationDto>(json);

            var occupied = occupation.Occupied ? "occupied" : "free";
            log.LogInformation($"New Occupation: {occupied}");

            return new OccupationEntity(occupation);
        }
    }
}
