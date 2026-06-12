// Lunar SaaS Interactive Application Engine

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initTerminalSimulator();
  initDocsSidebar();
  initCommandSearch();
  initAssertionValidator();
  initWaitlist();
  initContactForm();
  initViewerCount();
});

// ----------------------------------------------------
// 1. Navigation and Page Transitions
// ----------------------------------------------------
function initNavigation() {
  const docsSection = document.getElementById('documentation-section');
  const navDocsLink = document.getElementById('nav-docs-link');
  const btnFreeTier = document.getElementById('btn-free-tier');
  const heroBtnFree = document.getElementById('hero-btn-free');

  const showDocs = (e) => {
    if (e) e.preventDefault();
    docsSection.classList.remove('hidden');
    docsSection.scrollIntoView({ behavior: 'smooth' });
    
    // Trigger window resize event to force recalculation of any sticky layouts if necessary
    window.dispatchEvent(new Event('resize'));
  };

  if (navDocsLink) navDocsLink.addEventListener('click', showDocs);
  if (btnFreeTier) btnFreeTier.addEventListener('click', showDocs);
  if (heroBtnFree) heroBtnFree.addEventListener('click', showDocs);
}

// ----------------------------------------------------
// 2. Interactive CLI Terminal Simulator
// ----------------------------------------------------
function initTerminalSimulator() {
  const outputArea = document.getElementById('terminal-sim-output');
  const cmdButtons = document.querySelectorAll('.btn-term-cmd');
  
  let isRunning = false;

  const outputs = {
    init: `
<span class="text-cyan">[i] Initializing Lunar Project Workspace...</span>
<span class="text-muted">[?] Enter target API base URL:</span> https://dummyjson.com
<span class="text-muted">[?] Enter HuggingFace Hub Token (optional):</span> hf_****************

[+] Scanning project directory structure...
[+] Created lunar.config.json

<span class="text-success">[SUCCESS] Lunar workspace initialized successfully!</span>
<span class="text-cyan">[i] Run 'lunar config show' to verify configuration.</span>`,
    
    gen: `
<span class="text-cyan">[i] Probing endpoint: https://dummyjson.com/users ...</span>
[+] Detected content-type: application/json (status: 200 OK)
[+] Mapping JSON keys: [limit, skip, total, users]
[+] Extracting nested user schemas...

<span class="text-cyan">[i] Invoking Serverless HuggingFace LLM Engine (Qwen-2.5-Coder)...</span>
[+] Requesting CRUD suite cases generation...
[+] Model response received (took 1420ms)

[+] Compiling test assertion suites...
[+] Created file: <span class="text-cyan">lunar_tests/users.json</span> (5 test cases)
    - CASE 1: GET /users (Assert 200 OK, JSON schema)
    - CASE 2: POST /users (Assert 201 Created, body verification)
    - CASE 3: PUT /users/1 (Assert 200 OK, update checks)
    - CASE 4: DELETE /users/1 (Assert 200 OK, status check)
    - CASE 5: GET /users/99999 (Assert 404 Not Found, error verification)

<span class="text-success">[SUCCESS] AI Test suite generated! Run with 'lunar run'.</span>`,
    
    stress: `
<span class="text-cyan">[i] Initiating Concurrency Benchmark:</span>
    - Target Route: /users (https://dummyjson.com/users)
    - Request Capacity: 100 total requests
    - Concurrency level: 20 concurrent threads

[+] Spawning thread executors...
[||||||||||||||||||||||||||||||] 100% (100/100) | Speed: 48.2 req/sec

=======================================================
           BENCHMARK PERFORMANCE STATISTICS
=======================================================
Total Duration   : 2.07 seconds
Throughput (RPS) : <span class="text-cyan">48.24 RPS</span>

Latency Percentiles:
  p50 (Median)   : 412 ms
  p90            : 425 ms
  p95            : 432 ms
  p99 (Outliers) : <span class="text-error">489 ms</span>

HTTP Response Distribution:
  Status 200     : 100 requests (<span class="text-success">100.0%</span>)
  Status 4xx/5xx : 0 requests (0.0%)
=======================================================
<span class="text-success">[SUCCESS] Performance run completed.</span>`,
    
    run: `
<span class="text-cyan">[i] Finding test suites in lunar_tests/...</span>
<span class="text-cyan">[i] Found: lunar_tests/users.json</span>

=======================================================
             LUNAR CLI RUNNER: AUDIT REPORT
=======================================================
TEST CASE 1: GET /users
  <span class="text-success">[PASS]</span> Status code is 200
  <span class="text-success">[PASS]</span> Content-Type matches application/json
  <span class="text-success">[PASS]</span> JSON structure contains: ['users', 'total']
  <span class="text-success">[PASS]</span> Field types: 'total' is int, 'users' is list
  <span class="text-success">[PASS]</span> Response time: 312ms (SLA limit: 1500ms)

TEST CASE 2: POST /users
  <span class="text-success">[PASS]</span> Status code is 201
  <span class="text-success">[PASS]</span> Contains text: "id"
  <span class="text-success">[PASS]</span> Response time: 245ms (SLA limit: 1500ms)

TEST CASE 3: PUT /users/1
  <span class="text-success">[PASS]</span> Status code is 200
  <span class="text-success">[PASS]</span> JSON value checks: 'username' equals 'jane_doe'
  <span class="text-success">[PASS]</span> Response time: 289ms (SLA limit: 1500ms)

TEST CASE 4: DELETE /users/1
  <span class="text-success">[PASS]</span> Status code is 200
  <span class="text-success">[PASS]</span> Response time: 198ms (SLA limit: 1500ms)

TEST CASE 5: GET /users/99999
  <span class="text-success">[PASS]</span> Status code is 404
  <span class="text-success">[PASS]</span> Response time: 180ms (SLA limit: 1500ms)

-------------------------------------------------------
TEST RUN SUMMARY:
  Total Executed : 5 test suites
  Passed Checks  : 11 assertions
  Failed Checks  : 0 assertions
  Average Latency: 244.8 ms
=======================================================
<span class="text-success">[SUCCESS] All checks passed successfully!</span>`
  };

  const runCommandSim = (cmdType) => {
    if (isRunning) return;
    isRunning = true;
    
    // Disable command buttons
    cmdButtons.forEach(btn => btn.setAttribute('disabled', 'true'));
    
    const commandText = `lunar ${cmdType === 'init' ? 'init' : cmdType === 'gen' ? 'gen /users' : cmdType === 'stress' ? 'stress /users 100 20' : 'run'}`;
    outputArea.innerHTML = `<span class="term-prompt">lunar-cli $</span> <span id="typing-cmd"></span><span class="term-cursor">_</span>`;
    
    let charIdx = 0;
    const typingSpan = document.getElementById('typing-cmd');
    
    const typeInterval = setInterval(() => {
      if (charIdx < commandText.length) {
        typingSpan.textContent += commandText.charAt(charIdx);
        charIdx++;
      } else {
        clearInterval(typeInterval);
        
        // Show indicator and load output
        setTimeout(() => {
          outputArea.innerHTML = `<span class="term-prompt">lunar-cli $</span> <span>${commandText}</span>\n<span class="text-muted">Loading module dependencies...</span>`;
          
          setTimeout(() => {
            outputArea.innerHTML = `<span class="term-prompt">lunar-cli $</span> <span>${commandText}</span>\n` + outputs[cmdType] + `\n\n<span class="term-prompt">lunar-cli $</span> <span class="term-cursor">_</span>`;
            
            // Re-enable buttons
            cmdButtons.forEach(btn => btn.removeAttribute('disabled'));
            isRunning = false;
          }, 600);
        }, 300);
      }
    }, 45);
  };

  cmdButtons.forEach(button => {
    button.addEventListener('click', () => {
      const cmd = button.getAttribute('data-cmd');
      runCommandSim(cmd);
    });
  });
}

// ----------------------------------------------------
// 3. Documentation Sidebar and Navigation
// ----------------------------------------------------
function initDocsSidebar() {
  const links = document.querySelectorAll('.docs-nav-link');
  const pages = document.querySelectorAll('.docs-page');
  const pageNumIndicator = document.getElementById('docs-page-num');
  
  const btnPrev = document.getElementById('docs-btn-prev');
  const btnNext = document.getElementById('docs-btn-next');
  
  let currentIndex = 0;
  const pageCount = pages.length;

  const updatePaginationUI = () => {
    if (pageNumIndicator) {
      pageNumIndicator.textContent = `${currentIndex + 1} of ${pageCount}`;
    }
    
    // Toggle active link class
    links.forEach((link, idx) => {
      if (idx === currentIndex) {
        link.classList.add('active');
        // Scroll link into view inside sidebar on smaller screens
        link.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      } else {
        link.classList.remove('active');
      }
    });

    // Toggle active page display
    pages.forEach((page, idx) => {
      if (idx === currentIndex) {
        page.classList.add('active-page');
      } else {
        page.classList.remove('active-page');
      }
    });

    // Handle button disabled states
    if (btnPrev) {
      if (currentIndex === 0) {
        btnPrev.setAttribute('disabled', 'true');
      } else {
        btnPrev.removeAttribute('disabled');
      }
    }

    if (btnNext) {
      if (currentIndex === pageCount - 1) {
        btnNext.setAttribute('disabled', 'true');
      } else {
        btnNext.removeAttribute('disabled');
      }
    }
  };

  // Nav Links click
  links.forEach((link, index) => {
    link.addEventListener('click', () => {
      currentIndex = index;
      updatePaginationUI();
      document.getElementById('documentation-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  // Prev / Next click
  if (btnPrev) {
    btnPrev.addEventListener('click', () => {
      if (currentIndex > 0) {
        currentIndex--;
        updatePaginationUI();
        document.getElementById('documentation-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

  if (btnNext) {
    btnNext.addEventListener('click', () => {
      if (currentIndex < pageCount - 1) {
        currentIndex++;
        updatePaginationUI();
        document.getElementById('documentation-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

  // Initialize Code Copier
  const copyButtons = document.querySelectorAll('.btn-copy-code');
  copyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const textToCopy = btn.getAttribute('data-clipboard');
      navigator.clipboard.writeText(textToCopy).then(() => {
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        btn.style.color = 'var(--success-green)';
        btn.style.borderColor = 'var(--success-green)';
        
        setTimeout(() => {
          btn.textContent = originalText;
          btn.style.color = '';
          btn.style.borderColor = '';
        }, 1500);
      }).catch(err => {
        console.error('Failed to copy text: ', err);
      });
    });
  });

  // Set initial pagination UI
  updatePaginationUI();
}

// ----------------------------------------------------
// 4. Searchable Command Reference Table
// ----------------------------------------------------
function initCommandSearch() {
  const searchInput = document.getElementById('command-search-input');
  const tableRows = document.querySelectorAll('#command-reference-table tbody tr');

  if (!searchInput) return;

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    
    tableRows.forEach(row => {
      const commandCellText = row.querySelector('.cmd-cell').textContent.toLowerCase();
      const descriptionCellText = row.cells[2].textContent.toLowerCase();
      
      if (commandCellText.includes(query) || descriptionCellText.includes(query)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  });
}

// ----------------------------------------------------
// 5. Live Assertion Config JSON Validator
// ----------------------------------------------------
function initAssertionValidator() {
  const btnValidate = document.getElementById('btn-validate-schema');
  const jsonInput = document.getElementById('assertion-json-input');
  const statusBadge = document.getElementById('validator-status');
  const detailsBox = document.getElementById('validator-details');

  if (!btnValidate || !jsonInput) return;

  btnValidate.addEventListener('click', () => {
    const val = jsonInput.value.trim();
    
    if (!val) {
      statusBadge.textContent = 'Empty Input';
      statusBadge.className = 'status-badge status-idle';
      detailsBox.textContent = 'Please paste a JSON configuration to validate.';
      return;
    }

    try {
      const parsed = JSON.parse(val);
      
      // Ensure it is either an array of cases, or a single test case object
      const testCases = Array.isArray(parsed) ? parsed : [parsed];
      
      if (testCases.length === 0) {
        throw new Error("JSON should represent at least one test case object.");
      }

      // Check fields for each test case
      let parseWarnings = [];
      testCases.forEach((tCase, idx) => {
        const caseLabel = `Case #${idx + 1} (${tCase.name || 'Unnamed'})`;
        
        if (!tCase.endpoint) {
          parseWarnings.push(`- ${caseLabel}: Missing 'endpoint' key.`);
        }
        if (!tCase.method) {
          parseWarnings.push(`- ${caseLabel}: Missing 'method' key (GET, POST, etc).`);
        }
        
        if (tCase.assertions) {
          const ass = tCase.assertions;
          if (typeof ass !== 'object' || ass === null) {
            parseWarnings.push(`- ${caseLabel}: 'assertions' must be a JSON object.`);
          } else {
            // Validate assertion constraints
            if (ass.status_code && typeof ass.status_code !== 'number') {
              parseWarnings.push(`- ${caseLabel}: 'assertions.status_code' must be a numeric integer.`);
            }
            if (ass.contains_text && !Array.isArray(ass.contains_text)) {
              parseWarnings.push(`- ${caseLabel}: 'assertions.contains_text' must be a JSON array of strings.`);
            }
            if (ass.json_keys && !Array.isArray(ass.json_keys)) {
              parseWarnings.push(`- ${caseLabel}: 'assertions.json_keys' must be a JSON array of strings.`);
            }
            if (ass.max_response_time_ms && typeof ass.max_response_time_ms !== 'number') {
              parseWarnings.push(`- ${caseLabel}: 'assertions.max_response_time_ms' must be a numeric integer.`);
            }
            if (ass.json_types) {
              if (typeof ass.json_types !== 'object' || ass.json_types === null) {
                parseWarnings.push(`- ${caseLabel}: 'assertions.json_types' must be an object schema mapping fields to data types.`);
              } else {
                const validTypes = ['int', 'float', 'string', 'boolean', 'list', 'dict', 'array', 'object'];
                Object.entries(ass.json_types).forEach(([key, val]) => {
                  if (!validTypes.includes(val)) {
                    parseWarnings.push(`- ${caseLabel}: Type '${val}' for key '${key}' is invalid. Supported: ${validTypes.join(', ')}.`);
                  }
                });
              }
            }
          }
        } else {
          parseWarnings.push(`- ${caseLabel}: Recommended key 'assertions' is missing.`);
        }
      });

      if (parseWarnings.length > 0) {
        statusBadge.textContent = 'Validation Warnings';
        statusBadge.className = 'status-badge status-error';
        detailsBox.innerHTML = `<span class="text-error">JSON is valid structure, but fails Lunar specifications:</span>\n` + parseWarnings.join('\n');
      } else {
        statusBadge.textContent = 'Valid Config';
        statusBadge.className = 'status-badge status-success';
        
        let report = `<span class="text-success">[SUCCESS] Structure matches Lunar Engine specifications!</span>\n\n`;
        report += `Total parsed test cases: ${testCases.length}\n`;
        testCases.forEach((tCase, idx) => {
          report += `- Case ${idx + 1}: [${tCase.method || 'GET'}] ${tCase.endpoint || '/'}\n`;
          if (tCase.assertions) {
            const keys = Object.keys(tCase.assertions);
            report += `  Assertions checked: [${keys.join(', ')}]\n`;
          }
        });
        detailsBox.innerHTML = report;
      }

    } catch (err) {
      statusBadge.textContent = 'Syntax Error';
      statusBadge.className = 'status-badge status-error';
      detailsBox.innerHTML = `<span class="text-error">Failed to parse JSON:</span>\n${err.message}`;
    }
  });
}

// ----------------------------------------------------
// 6. Pro Waitlist Modal and Registration
// ----------------------------------------------------
function initWaitlist() {
  const modal = document.getElementById('waitlist-modal');
  const btnPro = document.getElementById('btn-pro-tier');
  const heroBtnPro = document.getElementById('hero-btn-pro');
  const btnClose = document.getElementById('btn-close-waitlist');
  const waitlistForm = document.getElementById('waitlist-form');
  const formContainer = document.getElementById('waitlist-form-container');
  const successContainer = document.getElementById('waitlist-success-container');
  const waitlistPosition = document.getElementById('waitlist-position');
  
  const showModal = (e) => {
    if (e) e.preventDefault();
    modal.classList.remove('hidden');
    
    // Check if user is already registered locally
    const savedWaitlist = localStorage.getItem('lunar_waitlist_registered');
    if (savedWaitlist) {
      const data = JSON.parse(savedWaitlist);
      formContainer.classList.add('hidden');
      successContainer.classList.remove('hidden');
      waitlistPosition.textContent = `#${data.position}`;
    } else {
      formContainer.classList.remove('hidden');
      successContainer.classList.add('hidden');
    }
  };

  const hideModal = () => {
    modal.classList.add('hidden');
  };

  if (btnPro) btnPro.addEventListener('click', showModal);
  if (heroBtnPro) heroBtnPro.addEventListener('click', showModal);
  if (btnClose) btnClose.addEventListener('click', hideModal);
  
  // Close when clicking background backdrop
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      hideModal();
    }
  });

  if (waitlistForm) {
    const submitBtn = document.getElementById('waitlist-submit');

    waitlistForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const emailInput = document.getElementById('waitlist-email');
      const email = emailInput.value.trim();
      
      if (!email) return;

      if (submitBtn) {
        submitBtn.textContent = 'Joining...';
        submitBtn.setAttribute('disabled', 'true');
      }

      // Post waitlist details to FormSubmit
      fetch("https://formsubmit.co/ajax/sodanapalliyashwanthreddy@gmail.com", {
        method: "POST",
        body: JSON.stringify({
          subject: "New Waitlist Registration - Lunar Cloud",
          email: email
        }),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        if (submitBtn) {
          submitBtn.textContent = 'Request Early Invitation';
          submitBtn.removeAttribute('disabled');
        }

        // Generate queue number
        const positionNum = Math.floor(Math.random() * 500) + 3120;
        
        // Save state to localStorage
        localStorage.setItem('lunar_waitlist_registered', JSON.stringify({
          email: email,
          position: positionNum,
          timestamp: new Date().toISOString()
        }));

        // Render success screen
        waitlistPosition.textContent = `#${positionNum.toLocaleString()}`;
        
        formContainer.classList.add('hidden');
        successContainer.classList.remove('hidden');
      })
      .catch(error => {
        if (submitBtn) {
          submitBtn.textContent = 'Request Early Invitation';
          submitBtn.removeAttribute('disabled');
        }
        console.error('Waitlist Submission Error:', error);
        alert("An error occurred. Please verify your connection and try again.");
      });
    });
  }
}

// ----------------------------------------------------
// 7. Contact Us Form Handling (FormSubmit AJAX API)
// ----------------------------------------------------
function initContactForm() {
  const contactForm = document.getElementById('contact-form');
  const formContainer = document.getElementById('contact-form-container');
  const successContainer = document.getElementById('contact-success-container');
  const submitBtn = document.getElementById('contact-submit');
  
  if (!contactForm || !submitBtn) return;

  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const name = document.getElementById('contact-name').value.trim();
    const email = document.getElementById('contact-email').value.trim();
    const subject = document.getElementById('contact-subject').value.trim();
    const message = document.getElementById('contact-message').value.trim();
    
    if (!name || !email || !subject || !message) return;

    // Set UI loading state
    submitBtn.textContent = 'Sending...';
    submitBtn.setAttribute('disabled', 'true');

    // Post to FormSubmit for sodanapalliyashwanthreddy@gmail.com
    fetch("https://formsubmit.co/ajax/sodanapalliyashwanthreddy@gmail.com", {
      method: "POST",
      body: JSON.stringify({
        name: name,
        email: email,
        subject: subject,
        message: message
      }),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      // Restore button state
      submitBtn.textContent = 'Send Message';
      submitBtn.removeAttribute('disabled');

      if (response.ok) {
        return response.json();
      } else {
        throw new Error("FormSubmit response was not OK");
      }
    })
    .then(data => {
      // Log locally for user convenience
      let submissions = [];
      const stored = localStorage.getItem('lunar_contact_submissions');
      if (stored) {
        submissions = JSON.parse(stored);
      }
      submissions.push({
        name,
        email,
        subject,
        message,
        timestamp: new Date().toISOString()
      });
      localStorage.setItem('lunar_contact_submissions', JSON.stringify(submissions));

      // Switch panel to success modal
      formContainer.classList.add('hidden');
      successContainer.classList.remove('hidden');
    })
    .catch(error => {
      submitBtn.textContent = 'Send Message';
      submitBtn.removeAttribute('disabled');
      console.error('Submission Error:', error);
      alert("Network error or invalid address setup. Please check your network and try again.");
    });
  });
}

// ----------------------------------------------------
// 8. Live Active Developers Counter (Real CounterAPI via Serverless API)
// ----------------------------------------------------
function initViewerCount() {
  const countEl = document.getElementById('viewer-count-val');
  if (!countEl) return;

  // Fetch the count from our Vercel serverless function (same-origin request)
  fetch('/api/visits')
    .then(response => {
      if (!response.ok) throw new Error('API Error');
      return response.json();
    })
    .then(data => {
      if (data && typeof data.value === 'number') {
        // Format the number with commas
        countEl.textContent = data.value.toLocaleString();
      } else {
        throw new Error('Invalid response data');
      }
    })
    .catch(error => {
      console.warn('Visits API failed, falling back to simulated local visits:', error);
      // Fallback: track visits in localStorage + base simulated count
      let visits = parseInt(localStorage.getItem('lunar_simulated_visits') || '384', 10);
      visits += 1;
      localStorage.setItem('lunar_simulated_visits', visits);
      countEl.textContent = visits.toLocaleString();
    });
}
