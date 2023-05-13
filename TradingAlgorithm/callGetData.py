from getData import GetData

get_data = GetData('1DAY', ['ETHUSDT', 'BTCUSDT'], 'separate', None)

get_data.collect_data()
