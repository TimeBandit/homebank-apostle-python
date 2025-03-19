from datetime import datetime
from termcolor import colored
from tabulate import tabulate


def display_rows_in_terminal(rows):
    """Display rows in terminal with color coding and formatting"""
    # Convert rows to a format suitable for tabulate
    formatted_rows = []

    for row in rows:
        # Color amount based on whether it's positive or negative
        amount = float(row['amount'])
        if amount > 0:
            amount_str = colored(f"+{amount:.2f}", 'green')
        else:
            amount_str = colored(f"{amount:.2f}", 'red')

        # Format date
        date = datetime.strptime(row['date'], '%d/%m/%Y').strftime('%Y-%m-%d')

        # Color code different payment types
        payment_type = row['payment']
        if payment_type == '9':  # Interest
            payee = colored(row['payee'], 'cyan')
        elif payment_type == '4':  # Rent
            payee = colored(row['payee'], 'yellow')
        else:
            payee = row['payee']

        formatted_row = [
            date,
            payment_type,
            payee,
            row['memo'],
            amount_str,
            row.get('category', ''),
            row.get('tags', '')
        ]
        formatted_rows.append(formatted_row)

    # Define headers
    headers = ['Date', 'Type', 'Payee', 'Memo', 'Amount', 'Category', 'Tags']

    # Print the table
    print("\n" + colored("Transaction Records:", 'white', attrs=['bold']))
    print(tabulate(formatted_rows, headers=headers, tablefmt='grid'))

    # Print summary
    total = sum(float(row['amount']) for row in rows)
    total_str = colored(
        f"+{total:.2f}", 'green') if total > 0 else colored(f"{total:.2f}", 'red')
    print(f"\nTotal Balance: {total_str}")
