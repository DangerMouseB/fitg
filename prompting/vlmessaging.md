

## msgArrived handler

- One per agent class

```Python
class AnAgent:
    
    REGISTER_TAKER = 'REGISTER_TAKER'   # takers are more secretive so no join / left protocol
    
    async def msgArrived(self, msg):
        if msg.subject == self.REGISTER_PROVIDER:
            providerName = msg.contents
            self.addrByProviderName[providerName] = msg.sender.addr
            await self.conn.send(msg.reply(True))
```

## schedule a callback
```Python
    conn.scheduleCallback(fn, after)
```

conn - vlmessaging.Connection object
fn - function to call back - no params
after - milliseconds to wait, datetime.datetime or datetime.timedelta


## blocking / synchronously send a message with timeout
```Python
    reply = await conn.send(msg, timeout)
```
reply will either be a vlmessaging.Message object or Missing if timed out


## non-blocking / asynchronously send a message
```Python
    await conn.send(msg)
```
sendMsg returns None in this case.


