for shop_id in shop3_keys:
    shop_df = df[df['shopid'] == shop_id]
    print(f'Shop id {shop_id} in progress....')
    cheated_id[shop_id] = []
    cheated_id_value[shop_id] = 0
    for shop in range(len(shop_df)):
        end_order = 0
        for ts in range(shop+1, len(shop_df)):   
            #print(f'shop = {shop} ts = {ts}')
            if (shop_df.iloc[ts]['timeStamp'] - shop_df.iloc[shop]['timeStamp'] > 3600) or (ts == len(shop_df)-1):
                if ((ts == len(shop_df)-1) and (shop_df.iloc[ts]['timeStamp'] - shop_df.iloc[shop]['timeStamp'] <= 3600)):
                    end_order = ts+1
                else :
                    end_order = ts
                break
        if ts-shop < 2:
            continue
        else :
            hour_interval = shop_df.iloc[shop: end_order]
            order_num = hour_interval.orderid.nunique()
            user_num = hour_interval.userid.nunique()
            #print(hour_interval)
            if order_num/user_num >= 3:
                print(f'Cheated Found!! Shopid {shop_id} is cheat!!!')
                cheated_shop[shop_id] = 1
                max_user = max(hour_interval.groupby('userid').size())
                user_list = hour_interval.groupby('userid').size()[hour_interval.groupby('userid').size() == max(hour_interval.groupby('userid').size())].keys().to_list()
                if max_user > cheated_id_value[shop_id]:
                    cheated_id_value[shop_id] = max_user
                    cheated_id[shop_id] = []
                    for userid in user_list:
                        print('Appending user in progress')
                        cheated_id[shop_id].append(userid)
                elif max_user == cheated_id_value[shop_id]:
                    for userid in user_list:
                        print('Appending user in progress')
                        cheated_id[shop_id].append(userid)
                else:
                    continue
