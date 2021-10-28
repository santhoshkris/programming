package com.twi.kotlinrestdemo.kotlinrestdemo

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/api")
class DemoRestController {

    @GetMapping("/hello")
    fun sayHello(@RequestParam name: List<String>): String {
        println("$name")
        return "Hello from Kotlin Controller....$name".uppercase()
    }
}