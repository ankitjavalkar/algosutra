
item_prices = {
  "milk" => {"label" => "Milk", "unit_price" => 3.97, "sale_price" => [2, 5.0]},
  "bread" => {"label" => "Bread", "unit_price" => 2.17, "sale_price" => [3, 6.0]},
  "banana" => {"label" => "Banana", "unit_price" => 0.99, "sale_price" => nil},
  "apple" => {"label" => "Apple", "unit_price" => 0.89, "sale_price" => nil},
}

def get_clean_input(item_list)
  item_list.split(",").each_with_object([]) do |item, array|
    array.push(item.strip.downcase)
  end
end

def get_item_count(item_list)
  item_list.each_with_object(Hash.new(0)) do |item, hash|
    hash[item] += 1
  end  
end

def calculate_price(item_count, item_prices)
  saved = 0.0
  hash = Hash.new(0)
  item_count.each do |item, buy_qty|
    begin
      uprice = item_prices[item]["unit_price"]
      original_cost = buy_qty * uprice

      unless item_prices[item]["sale_price"].nil?
        sale_price = item_prices[item]["sale_price"][1]
        sale_price_qty = item_prices[item]["sale_price"][0]
        if buy_qty >= sale_price_qty
          hash[item] += sale_price
          buy_qty = buy_qty - sale_price_qty
        end
      end
 
      hash[item] += (buy_qty * uprice)
      saved += original_cost - hash[item]
    rescue KeyError => e
      puts("This item is not in the price list")
    end
  end
  return hash, saved
end

def format_output(final_price, item_count, saved)
  puts("Item\t\tQuantity\t\tPrice\n")
  final_price.each do |item, price|
    puts("#{item}\t\t#{item_count[item]}\t\t#{price}")
  end
  puts("You saved: #{saved}")
end

puts "Please enter all the items seperated by a comma:"
item_list = gets

clean_item_array = get_clean_input(item_list)
item_count = get_item_count(clean_item_array)
final_price, saved = calculate_price(item_count, item_prices)
puts "This is list!  - End\n\n", final_price
format_output(final_price, item_count, saved)
