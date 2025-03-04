//
//  unhinged_appUITests.swift
//  unhinged appUITests
//
//  Created by Harry Sho on 11/7/24.
//

import XCTest
@testable import unhinged_app

final class unhinged_appUITests: XCTestCase {

    override func setUpWithError() throws {
        // Put setup code here. This method is called before the invocation of each test method in the class.
        super.setUp()
        // In UI tests it is usually best to stop immediately when a failure occurs.
        continueAfterFailure = false

        // In UI tests it’s important to set the initial state - such as interface orientation - required for your tests before they run. The setUp method is a good place to do this.
    }

    override func tearDownWithError() throws {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
    }

    func testNoAppleIDShowsAlert() throws {
        let app = XCUIApplication()
        app.launch()
        
        let loginButton = app.buttons["Sign in with Apple"]
        XCTAssertTrue(loginButton.exists, "The 'Login with Apple' button should exist.")
        loginButton.tap()
    }


    func testLaunchPerformance() throws {
        if #available(macOS 10.15, iOS 13.0, tvOS 13.0, watchOS 7.0, *) {
            // This measures how long it takes to launch your application.
            measure(metrics: [XCTApplicationLaunchMetric()]) {
                XCUIApplication().launch()
            }
        }
    }
}
