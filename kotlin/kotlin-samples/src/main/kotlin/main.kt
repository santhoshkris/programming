
fun main() {
    println(findCustomers().map { it.name }.toMutableList())
}
data class Customer (val id: Int, val name: String, val email: String)

fun findCustomers(): List<Customer> {
    val customers = mutableListOf<Customer>()
    customers.add(Customer(1,"San","san@san.com"))
    customers.add(Customer(2,"Sandy", "sandy@san.com"))
    return customers
}