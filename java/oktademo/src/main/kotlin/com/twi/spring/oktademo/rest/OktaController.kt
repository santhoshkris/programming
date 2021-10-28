package com.twi.spring.oktademo.rest


import org.springframework.security.core.annotation.AuthenticationPrincipal
import org.springframework.security.oauth2.core.oidc.user.OidcUser
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController

class OktaController {

    @GetMapping("/greet")
    fun greet(@AuthenticationPrincipal user: OidcUser): String{
        val name = user.givenName
        return "Hello $name from the Controller"
    }

}