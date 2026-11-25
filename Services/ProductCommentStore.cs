using System.Collections.Concurrent;
using System.Threading.Channels;
using WebApplication2.Models;

namespace WebApplication2.Services;

public sealed class ProductCommentStore
{
    private readonly ConcurrentDictionary<string, ConcurrentDictionary<Guid, Channel<ProductComment>>> _subscribers = new(StringComparer.OrdinalIgnoreCase);

    public void PublishComment(ProductComment comment)
    {
        if (_subscribers.TryGetValue(comment.ProductSlug, out var subscribers))
        {
            foreach (var channel in subscribers.Values)
            {
                channel.Writer.TryWrite(comment);
            }
        }

    }

    public (Guid Id, ChannelReader<ProductComment> Reader) Subscribe(string productSlug)
    {
        var channel = Channel.CreateBounded<ProductComment>(new BoundedChannelOptions(32)
        {
            FullMode = BoundedChannelFullMode.DropOldest,
            SingleReader = true,
            SingleWriter = false
        });
        var id = Guid.NewGuid();
        _subscribers.GetOrAdd(productSlug, _ => new ConcurrentDictionary<Guid, Channel<ProductComment>>())[id] = channel;
        return (id, channel.Reader);
    }

    public void Unsubscribe(string productSlug, Guid id)
    {
        if (_subscribers.TryGetValue(productSlug, out var subscribers) && subscribers.TryRemove(id, out var channel))
        {
            channel.Writer.TryComplete();
        }
    }
}
