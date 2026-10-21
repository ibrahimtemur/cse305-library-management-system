/*
 * Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
 * Student No(s)#: 231805033, 231805026
 * General Comments: Smoke test verifying that the Spring application context loads cleanly.
 */
package edu.adu.lms;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class LibraryManagementApplicationTests {

    @Test
    @DisplayName("Spring application context loads without errors")
    void contextLoads() {
        // Verifies that the Spring Boot context initializes with JPA, H2, Web, Validation, and Thymeleaf.
    }
}
