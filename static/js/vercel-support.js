// This file will handle multi-device synchronization for our Vercel deployment
console.log('Vercel Support Script Loaded');

// Additional enhancements for Vercel deployment
(function() {
    // Fix CSRF issues on Vercel
    function fixCsrfForVercel() {
        // Get CSRF token from cookie for Vercel environments
        function getCsrfTokenFromCookie() {
            const name = 'csrftoken=';
            const decodedCookie = decodeURIComponent(document.cookie);
            const cookieArray = decodedCookie.split(';');
            for(let i = 0; i < cookieArray.length; i++) {
                let cookie = cookieArray[i];
                while (cookie.charAt(0) === ' ') {
                    cookie = cookie.substring(1);
                }
                if (cookie.indexOf(name) === 0) {
                    return cookie.substring(name.length, cookie.length);
                }
            }
            return '';
        }
        
        // Set the CSRF token in meta tag if it exists in cookies but not in meta
        const csrfCookie = getCsrfTokenFromCookie();
        let metaTag = document.querySelector('meta[name="csrf-token"]');
        
        if (csrfCookie && (!metaTag || !metaTag.getAttribute('content'))) {
            if (!metaTag) {
                metaTag = document.createElement('meta');
                metaTag.setAttribute('name', 'csrf-token');
                document.head.appendChild(metaTag);
            }
            metaTag.setAttribute('content', csrfCookie);
            console.log('CSRF token updated from cookie for Vercel compatibility');
        }
    }
    
    // Handle multi-device login
    function unifyLocalStorage() {
        const currentUsername = document.querySelector('[data-username]')?.getAttribute('data-username');
        if (!currentUsername) return;
        
        const keys = Object.keys(localStorage);
        const transactionKeys = keys.filter(key => key.startsWith('budgetTracker_transactions_'));
        
        if (transactionKeys.length > 1) {
            console.log('Multiple transaction storage keys found, unifying...');
            
            // Current user's storage key
            const currentKey = `budgetTracker_transactions_${currentUsername}`;
            let allTransactions = [];
            
            // Collect all transactions
            transactionKeys.forEach(key => {
                const transactions = JSON.parse(localStorage.getItem(key) || '[]');
                allTransactions = [...allTransactions, ...transactions];
            });
            
            // Remove duplicates
            allTransactions = allTransactions.filter((transaction, index, self) =>
                index === self.findIndex((t) => t.id === transaction.id)
            );
            
            // Sort by date
            allTransactions.sort((a, b) => new Date(b.date_created) - new Date(a.date_created));
            
            // Save unified transactions to current user's key
            localStorage.setItem(currentKey, JSON.stringify(allTransactions));
            
            // Clean up old keys (except current)
            transactionKeys.forEach(key => {
                if (key !== currentKey) {
                    localStorage.removeItem(key);
                }
            });
            
            console.log(`Unified ${allTransactions.length} transactions under ${currentUsername}`);
        }
    }
    
    // Setup heartbeat to keep session alive on Vercel
    function setupSessionHeartbeat() {
        setInterval(() => {
            fetch('/health/', { 
                method: 'GET',
                credentials: 'include'
            })
            .then(response => response.json())
            .then(data => {
                console.log('Session heartbeat: ', data.status === 'ok' ? 'OK' : 'Failed');
            })
            .catch(error => {
                console.error('Session heartbeat failed: ', error);
            });
        }, 60000); // Every minute
    }
    
    // Initialize Vercel enhancements
    document.addEventListener('DOMContentLoaded', function() {
        // Add username data attribute for script use
        const usernameElement = document.querySelector('p.text-gray-300.text-sm');
        if (usernameElement) {
            const username = usernameElement.textContent.replace('Welcome back, ', '').replace('!', '');
            usernameElement.setAttribute('data-username', username);
        }
        
        setTimeout(() => {
            fixCsrfForVercel();
            unifyLocalStorage();
            setupSessionHeartbeat();
        }, 1000);
    });
})();
