const config = {
  "params": {                       // Client-side parameters
    "required": [                     // REQUIRED LOG parameters (have to start with 'log.')
      "log.test_info",                  // Information about the test-step
      "log.env_tester",                 // Environment of the test machine (i.e. `local`, `grid`, `saucelabs`, `iphone 7`, `galaxy-s6`, etc.)
      "log.team",                       // The name of the test team (this is used to organize the Kibana dashboard)
      "log.browser",                    // The browser used to perform the test (i.e. `Chrome`, `FireFox`, etc. - for API tests, use something like `api-curl`)
      "log.env_target"                  // Environment of the target application (i.e. `dev`, `test`, `prod`)
    ],
    "defaults": {                     // DEFAULT parameters (will be used if they are not provided in the client's POST body)
      "baseline": {                     // These settings are used to calculate the baseline
        "days": 7,                        // Number of days to calculate the baseline for (default: 7)
        "perc": 75,                       // Percentile to calculate (default: 75)
        "padding": 1.2                    // Multiplier to calculate extra padding on top of the baseline (default: 1.2 = 20%)
      },
      "flags": {                        // These booleans determine the output and other actions to be performed
        "assertBaseline": true,           // Whether or not to compare against baseline (default: true)
        "debug": false,                   // Request extra debug info from the API (default: false)
        "esTrace": false,                 // Request elasticsearch output from API (default: false)
        "esCreate": false,                // Save results to elasticsearch (default: false)
        "passOnFailedAssert": false       // Pass the test, even when the performance is above the threshold (default: false)
      }
    }
  }
}

module.exports = config;