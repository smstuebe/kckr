using System;
using Microsoft.WindowsAzure.Storage.Table;

namespace Kckr.Functions
{
    public class ReverseOrderedDeviceEntity : TableEntity
    {
        public ReverseOrderedDeviceEntity(DeviceDto dto)
        {
            PartitionKey = dto.Location;
            RowKey = (DateTime.MaxValue.Ticks - DateTime.UtcNow.Ticks).ToString("D19");
        }
    }
}
