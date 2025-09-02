# This prompt is designed to guide an Autonomous Agent in editing and generating code within a Python FastAPI project, ensuring adherence to best practices, autonomous testing, and automatic documentation updates.

## Core Principles

When editing or generating code, ALWAYS prioritize the following principles:

- **Single Responsibility Principle (SRP):** Each function, class, or module should have one, and only one, reason to change.
- **Open/Closed Principle (OCP):** Code should be open for extension but closed for modification. Use inheritance or interfaces to add functionality without altering existing code.
- **Liskov Substitution Principle (LSP):** Subtypes must be substitutable for their base types without affecting correctness.
- **Interface Segregation Principle (ISP):** Clients should not be forced to depend on interfaces they don't use. Favor smaller, specific interfaces.
- **Dependency Inversion Principle (DIP):** High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details. Details should depend on abstractions.
- **Keep it Simple, Stupid (KISS):** Favor simplicity over complexity.
- **You Ain't Gonna Need It (YAGNI):** Don't add functionality until it's actually needed.
- **Don't Repeat Yourself (DRY):** Avoid duplicating code. Extract common logic into reusable functions or classes.
- **Separation of Concerns (SoC):** Separate concerns like data access, business logic, and presentation.
- **Principle of Least Astonishment (POLA):** Code should behave as expected, following common conventions.

## FastAPI Specific Guidelines

- **Asynchronous Operations:** Utilize `async` and `await` for I/O-bound operations to maximize performance.
- **Pydantic Models:** Use Pydantic models for data validation, serialization, and documentation. Define clear input and output schemas.
- **Dependency Injection:** Leverage FastAPI's dependency injection system for managing dependencies and improving testability.
- **Path Operations:** Use appropriate HTTP methods (GET, POST, PUT, DELETE, etc.) for path operations.
- **Error Handling:** Implement robust error handling using FastAPI's exception handling mechanisms. Return appropriate HTTP status codes and error messages.
- **Middleware:** Use middleware for cross-cutting concerns like authentication, logging, and request processing.
- **Security:** Implement security measures such as authentication, authorization, and input validation to protect against vulnerabilities.
- **Background Tasks:** Use background tasks for long-running or non-critical operations.
- **Streaming Responses:** Use streaming responses for large datasets or real-time data.
- **WebSockets:** Implement WebSocket endpoints for real-time communication.

## Documentation & Static Analysis

- **Automatic API Documentation (Swagger/OpenAPI):** Ensure that all endpoints are automatically documented using FastAPI's built-in Swagger/OpenAPI support. Review and enhance the generated documentation as needed.
- **Docstrings:** Write clear and concise docstrings for all functions, classes, and methods. Follow the Google Python Style Guide for docstring formatting.
- **Type Hints & MyPy:** Use type hints extensively to improve code readability and enable static analysis. All code must pass `mypy` static type checking as configured in `mypy.ini` and `pyproject.toml`. This ensures type safety and reduces runtime errors.
- **Model Documentation (Pydantic & SQLAlchemy):**
  - All Pydantic models (request/response schemas) should have clear class-level docstrings explaining their purpose.
  - Each field within a Pydantic model should include a `description` parameter (e.g., `Field(..., description="Your descriptive text here")`) to ensure it appears in the OpenAPI schema and is clear to other developers.
  - SQLAlchemy models (database tables) should have clear class-level docstrings explaining the table's purpose.
  - Individual SQLAlchemy columns (attributes in the model) should have explanatory comments if their purpose or constraints are not immediately obvious from the name and type.
- **Backstage Documentation (`mkdocs.yml` & `catalog-info.yaml`):** When adding new features or modules, update the documentation navigation in `mkdocs.yml`. Review and update `catalog-info.yaml` with relevant tags, links, or description changes to keep the Backstage portal current.
- **Update Documentation:** Whenever code is modified, ensure that the documentation is updated accordingly. This includes updating docstrings, API documentation, and any relevant README files.
- **Test Documentation:** Document test cases and scenarios in the test files:
  - Purpose of each test class and method
  - Test data preparation and assumptions
  - Expected outcomes and assertions
  - Special setup or cleanup requirements

## Testing Guidelines

- **Test Structure:** Follow the existing test pattern using pytest fixtures and the AAA (Arrange-Act-Assert) pattern.
- **Test Coverage:** Strive for a high degree of test coverage. The project enforces a minimum of 90% test coverage, as configured in `pytest.ini`. After running tests, you can inspect the detailed HTML coverage report in the `coverage_html/` directory to identify any gaps. This includes:

  - Unit tests for individual components (functions, classes).
  - Integration tests for interactions between components (e.g., API endpoints testing business logic and database interaction).
  - End-to-end tests for complete user workflows (use judiciously, as they are more expensive to maintain).
  - Edge cases, error scenarios, and security vulnerabilities.
    Focus on ensuring critical paths and core functionalities are thoroughly tested.

- **Test Organization:**

  ```python
  class TestFeatureName:
      @pytest.mark.asyncio
      async def test_specific_functionality(self, client: AsyncClient): # Or other relevant fixtures
          # Arrange: Setup test data, mocks, and preconditions
          test_data = {...}
          # e.g., mock_db_call.return_value = ...

          # Act: Execute the code being tested
          response = await client.post("/endpoint", json=test_data)

          # Assert: Verify the outcome
          assert response.status_code == 200
          assert response.json() == expected_result
  ```

- **Mock Dependencies:** Use pytest fixtures and mocking (`unittest.mock.patch`, `MagicMock`) effectively to isolate components under test. This is crucial for unit tests.

  - Mock database calls to test service logic without actual DB operations.
  - Mock external service APIs.
  - Mock authentication/authorization layers when testing specific business logic.

- **Test Categories (Ensure coverage across these):**

  - **Success Cases:** Test the "happy path" with valid inputs and expected behavior.
  - **Failure Cases:** Test how the system handles invalid inputs, errors, and exceptions (e.g., validation errors, resource not found).
  - **Edge Cases:** Test boundary conditions, empty inputs, large inputs, and other unusual but valid scenarios.
  - **Security Tests:** (If applicable) Test for common vulnerabilities like unauthorized access, input sanitization issues (though FastAPI helps a lot here).
  - **Performance Tests:** (Separate suite, typically) Test response times and resource usage under load for critical endpoints.

- **Best Practices for Writing Effective and Maintainable Tests:**
  - **Keep tests independent and isolated:** Each test should be runnable on its own and not depend on the state or outcome of other tests. Use proper setup and teardown in fixtures.
  - **Test one specific behavior per test case:** A single test method should verify one logical outcome or scenario. This makes tests easier to understand and debug.
  - **Test behavior, not implementation details:** Focus on _what_ the code should do (its public contract/API) rather than _how_ it does it. This makes tests less brittle and more resilient to refactoring.
  - **Write clear and descriptive test names:** Names should clearly indicate what scenario is being tested (e.g., `test_create_item_successfully`, `test_create_item_fails_if_name_is_duplicate`).
  - **Use the AAA pattern consistently:** (Arrange, Act, Assert) for readability.
  - **Use fixtures effectively:** For shared setup (like a test client, mock database session) and to manage test data.
  - **Prioritize and Avoid Unnecessary Tests to Reduce Complexity:**
    - Focus testing efforts on critical business logic, complex algorithms, and high-risk areas.
    - Avoid writing tests for trivial getter/setter methods that don't contain any logic.
    - Do NOT test the internals of third-party libraries (e.g., don't test if SQLAlchemy correctly commits a transaction). Instead, test _your code's integration_ with those libraries (e.g., that your service method calls `session.commit()`).
    - Be cautious about tests that are too closely tied to the current implementation details, as they might break frequently during refactoring without indicating a real bug.
    - Strive for a balance: high coverage is good, but not at the cost of unmaintainable or low-value tests.
  - **Use parameterized tests (`@pytest.mark.parametrize`)** to efficiently test the same logic with multiple different inputs and expected outputs.
  - **Ensure test data is minimal and relevant** to the scenario being tested. Avoid using overly complex or large data objects if simpler ones suffice.
  - **Add comments sparingly:** Well-named tests and clear assertions should make the test's purpose obvious. Use comments only for explaining complex setups or non-obvious reasoning.

## Instructions for Autonomous Agents

1.  **Deconstruct the Goal:** Break down the high-level objective into a sequence of smaller, verifiable steps. Plan the implementation, testing, and documentation phases.
2.  **Execute Systematically:** Address one file or one concern at a time. Read existing code to understand the context before modifying it.
3.  **Adhere to Blueprints:** Strictly follow the core principles and FastAPI-specific guidelines outlined in this document.
4.  **Self-Correction through Testing:** After implementing a change, run existing tests to check for regressions. Write new unit and integration tests to validate the new functionality. If tests fail, analyze the errors and correct the code.
5.  **Document Diligently:** After verifying the code changes, update all relevant documentation, including docstrings, type hints, and schema descriptions (`description` fields in Pydantic models).
6.  **Report Completion:** Once all steps are successfully completed and verified, summarize the changes made, the tests passed, and confirm the completion of the overall goal.

## Example Scenarios for Autonomous Agents

- **High-Level Goal:** "Implement a feature to allow users to reset their passwords. This should involve generating a reset token, sending an email, and providing an endpoint to set a new password."
- **Agent's Plan:**
  1.  Create a new Pydantic schema for the password reset request.
  2.  Implement a function to generate a secure, short-lived password reset token.
  3.  Add a new endpoint `/password-reset-request` that takes a user's email, generates a token, and (simulates) sending an email.
  4.  Add a new endpoint `/password-reset` that takes the token and a new password, validates the token, and updates the user's password in the database.
  5.  Write unit tests for token generation and validation logic.
  6.  Write integration tests for the two new endpoints, covering success and failure cases (e.g., invalid token, expired token).
  7.  Update all docstrings and OpenAPI schema descriptions for the new code.
  8.  Run all project tests to ensure no regressions were introduced.
  9.  Report successful implementation.

## Important Considerations

- **Security:** Always prioritize security when writing code. Be aware of common vulnerabilities and take steps to mitigate them.
- **Performance:** Optimize code for performance, but only after identifying bottlenecks.
- **Scalability:** Design the application to be scalable to handle increasing traffic and data volumes.

## Example Test Scenarios

- **API Endpoint Testing:**

  ```python
  async def test_create_user_success(self, client: AsyncClient):
      # Arrange
      user_data = {"username": "test_user", "email": "test@example.com"}

      # Act
      response = await client.post("/users/", json=user_data)

      # Assert
      assert response.status_code == 201
      assert response.json()["username"] == user_data["username"]
  ```

- **Error Handling Testing:**

  ```python
  async def test_create_user_duplicate_email(self, client: AsyncClient):
      # Arrange
      existing_user = {"username": "existing", "email": "existing@example.com"}
      await client.post("/users/", json=existing_user)

      # Act
      response = await client.post("/users/", json=existing_user)

      # Assert
      assert response.status_code == 400
      assert "email already exists" in response.json()["detail"]
  ```
