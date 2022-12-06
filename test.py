import friartuck

if __name__ == "__main__":
    ft = friartuck.FriarTuck()
    print(ft.open_option_orders())
    print(ft.cancel_option_order_by_id("638901f4-7822-4f09-8c68-b03445a673f9"))
    print(ft.open_option_orders())
