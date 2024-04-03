from dbConnections import sql_select_queries as sql_queries


def get_orders():
    orders = sql_queries.get_orders()
    orders = [create_order(order) for order in orders]
    return orders


def create_order(order):
    ord = {'id': order['row'][0], 'orderCode': order['row'][1], 'orderDesc': order['row'][2],
           'checkIn': order['row'][3], 'checkOut': order['row'][4],
           'price': order['row'][10], 'orderId': order['row'][15], 'orderSegmentId': order['row'][16], 'orderSegId': order['row'][17],
           'createDate': order['row'][18], 'roomClassCode': order['row'][20], 'roomClassDesc': order['row'][20], 'city': order['row'][21]}
    print('ord:', ord)
    return ord
