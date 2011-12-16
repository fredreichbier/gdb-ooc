doStuff: func ~s (s: String) { s println() }
doStuff: func ~b (b: Buffer) { "Yow, I got a buffer at %p" printfln(b) }

doStuff("hai")

data := gc_malloc(UInt8 size * 4) as UInt8*
data[0] = 0xde
data[1] = 0xad
data[2] = 0xbe
data[3] = 0xef
b := Buffer new()
b append(data as Char*, 4)

doStuff(b)
