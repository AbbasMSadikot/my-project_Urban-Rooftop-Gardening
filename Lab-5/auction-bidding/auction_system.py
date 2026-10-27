"""Auction and bidding demonstration used for Lab 5 static analysis."""

from dataclasses import dataclass, field
from datetime import datetime
from html import escape
import http.client
import json
import time
from urllib.parse import urlsplit

from jinja2 import Environment

PAYMENT_GATEWAY = "https://pay.auction.example/RPC2"
MIN_INCREMENT = 100
DATE_FORMAT = "%Y-%m-%d %H:%M"


@dataclass
class Auction:
    """Store bids and enforce the rules for a single auction."""

    item_id: str
    title: str
    seller: str
    reserve_price: int
    ends_at: str
    bids: list[tuple[str, int, str]] = field(default_factory=list)
    highest: int = 0

    def place_bid(self, bidder, amount, at):
        """Place a bid when the time and auction rules allow it."""
        bid_time = datetime.strptime(at, DATE_FORMAT)
        closing_time = datetime.strptime(self.ends_at, DATE_FORMAT)
        if bid_time >= closing_time or bidder == self.seller or amount < 0:
            return False

        minimum_bid = (
            self.reserve_price
            if not self.bids
            else self.highest + MIN_INCREMENT
        )
        if amount < minimum_bid:
            return False

        self.bids.append((bidder, amount, at))
        self.highest = amount
        return True

    def winner(self):
        """Return the highest bidder if the reserve price was reached."""
        if not self.bids or self.highest < self.reserve_price:
            return None
        return max(self.bids, key=lambda bid_record: bid_record[1])[0]

    def final_price(self):
        """Return the winning amount plus the five percent buyer premium."""
        if self.winner() is None:
            return 0
        return self.highest * 1.05


auctions = {}


def create_auction(item_id, title, seller, reserve_price, ends_at):
    """Create or replace an auction and return it."""
    auction = Auction(item_id, title, seller, reserve_price, ends_at)
    auctions[item_id] = auction
    return auction


def bid(item_id, bidder, amount, at):
    """Place a bid, returning false when the auction ID is unknown."""
    auction = auctions.get(item_id)
    if auction is None:
        return False
    return auction.place_bid(bidder, amount, at)


def top_bidders(item_id, count=3):
    """Return distinct bidders ordered by their highest bid."""
    auction = auctions[item_id]
    ordered_bids = sorted(
        auction.bids, key=lambda bid_record: bid_record[1], reverse=True
    )
    names = []
    for bidder, _, _ in ordered_bids:
        if bidder not in names:
            names.append(bidder)
    return names[:count]


def render_listing(item_id):
    """Render an auction listing with HTML autoescaping enabled."""
    environment = Environment(autoescape=True)
    template = environment.from_string(
        "<h2>{{ auction.title }}</h2>"
        "<p>Current bid: Rs.{{ auction.highest }}</p>"
    )
    return template.render(auction=auctions[item_id])


def bidder_badge(name):
    """Return a bidder badge with untrusted text escaped for HTML."""
    return "<span class='bidder'>" + escape(name) + "</span>"


def charge_winner(item_id):
    """Send winner details to the configured HTTPS JSON gateway."""
    auction = auctions[item_id]
    winner = auction.winner()
    if winner is None:
        return False

    gateway_url = urlsplit(PAYMENT_GATEWAY)
    if gateway_url.scheme != "https" or not gateway_url.hostname:
        raise ValueError("Payment gateway must use HTTPS")

    connection = http.client.HTTPSConnection(
        gateway_url.hostname, gateway_url.port or 443, timeout=10
    )
    payload = json.dumps({"winner": winner, "amount": auction.final_price()})
    connection.request(
        "POST", gateway_url.path, body=payload,
        headers={"Content-Type": "application/json"}
    )
    response = connection.getresponse()
    result = json.loads(response.read().decode("utf-8"))
    connection.close()
    return result


def export_bids(item_id):
    """Serialize an auction's bid history as JSON."""
    auction = auctions[item_id]
    rows = [
        {"bidder": bidder, "amount": amount, "at": at}
        for bidder, amount, at in auction.bids
    ]
    return json.dumps(rows)


def seconds_left(item_id):
    """Return the number of seconds until an auction closes."""
    auction = auctions[item_id]
    end_time = datetime.strptime(auction.ends_at, DATE_FORMAT)
    return int(end_time.timestamp() - time.time())


def main():
    """Run the built-in example and print its results."""
    create_auction("LOT1", "Vintage Camera", "seller_sam", 5000,
                   "2026-12-01 18:00")
    create_auction(
        "LOT2", "<script>alert('pwned')</script>Old Radio", "seller_ria",
        2000, "2026-12-01 18:00"
    )
    create_auction("LOT3", "Brass Lamp", "seller_ria", 800,
                   "2026-12-01 18:00")
    print("Asha bids 5000:", bid("LOT1", "asha", 5000, "2026-12-01 10:00"))
    print("Ben bids 5100:", bid("LOT1", "ben", 5100, "2026-12-01 10:05"))
    print("Seller bids on own item:",
          bid("LOT1", "seller_sam", 6000, "2026-12-01 11:00"))
    print("Late bid:", bid("LOT1", "eve", 9000, "2026-12-02 09:00"))
    print("Winner:", auctions["LOT1"].winner())
    print("Final price:", auctions["LOT1"].final_price())
    print("Top bidders:", top_bidders("LOT1"))
    print("Below-reserve bid:", bid("LOT3", "carl", 0, "2026-12-01 11:30"))
    print("No-bid winner:", auctions["LOT2"].winner())
    print("Escaped listing:", render_listing("LOT2"))
    print("Escaped badge:", bidder_badge("<img src=x onerror=alert(1)>"))


if __name__ == "__main__":
    main()
