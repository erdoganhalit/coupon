#from utils import parse_html_file
#from graph.graph import CouponCodesGraph
#
#cart_page = parse_html_file(file_path="test\\html_files\\amazon_cart.html")
#checkout_page = parse_html_file(file_path="test\\html_files\\amazon_checkout.html")
#
#graph = CouponCodesGraph()
#
#graph.stream_graph_updates(user_input=checkout_page)

from utils import parse_html_file
from graph.graph import CouponCodesGraph

def main():
    # Parse HTML files for cart and checkout pages
    cart_page = parse_html_file(file_path="test\\html_files\\amazon_cart.html")
    checkout_page = parse_html_file(file_path="test\\html_files\\amazon_checkout.html")

    # Initialize the graph
    graph = CouponCodesGraph()

    state = {"messages": []}

    print("Welcome! I can assist you with finding coupon codes. Type 'TERMINATE CONVERSATION' to end.")

    user_input = checkout_page  # Start with the checkout page input
    while True:
        # Stream updates through the graph
        graph.stream_graph_updates(user_input=user_input, state=state)

        # Ask for further user input
        user_input = input("\nYour response: ").strip()

        # Check if the user wants to terminate the conversation
        if user_input.upper() == "TERMINATE CONVERSATION":
            print("Goodbye! Have a great day!")
            break

if __name__ == "__main__":
    main()


