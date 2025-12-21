from collections import OrderedDict


simple_funnel_data = OrderedDict(
    input=110,
    registration=80,
    cart=40,
    checkout=20,
    retention=12,
)
rich_funnel_data = OrderedDict(
    input=OrderedDict(src1=50, src2=40, src3=20),
    registration=80,
    cart=40,
    checkout=20,
    retention=12,
)
