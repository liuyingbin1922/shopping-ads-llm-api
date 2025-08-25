/**
 * Analytics Beacon Library
 * 
 * A lightweight analytics library that uses navigator.sendBeacon for reliable data collection.
 */

class AnalyticsBeacon {
    constructor(options = {}) {
        this.baseUrl = options.baseUrl || 'http://localhost:8000/api/v1/beacon';
        this.userId = options.userId || null;
        this.sessionId = options.sessionId || this.generateSessionId();
        this.enabled = options.enabled !== false;
        this.debug = options.debug || false;
        
        this.init();
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    init() {
        if (!this.enabled) return;
        
        this.setupPageUnloadTracking();
        this.trackPageView();
        this.log('Analytics initialized');
    }
    
    setupPageUnloadTracking() {
        window.addEventListener('beforeunload', (event) => {
            this.track('page_unload', {
                page_url: window.location.href,
                time_on_page: this.getTimeOnPage()
            });
        });
    }
    
    trackPageView() {
        this.track('page_view', {
            page_url: window.location.href,
            page_title: document.title,
            referrer: document.referrer
        });
    }
    
    track(eventName, properties = {}) {
        if (!this.enabled) return;
        
        const eventData = {
            event_type: 'custom',
            event_name: eventName,
            user_id: this.userId,
            session_id: this.sessionId,
            page_url: window.location.href,
            properties: {
                ...properties,
                timestamp: new Date().toISOString()
            }
        };
        
        this.sendBeacon(eventData);
        this.log('Event tracked:', eventName);
    }
    
    sendBeacon(data) {
        try {
            if (navigator.sendBeacon) {
                const blob = new Blob([JSON.stringify(data)], {
                    type: 'application/json'
                });
                
                const success = navigator.sendBeacon(this.baseUrl + '/beacon', blob);
                
                if (success) {
                    this.log('Data sent via sendBeacon');
                    return true;
                }
            }
            
            this.sendViaFetch(data);
            
        } catch (error) {
            this.log('Error sending beacon:', error);
            this.sendViaFetch(data);
        }
    }
    
    async sendViaFetch(data) {
        try {
            const response = await fetch(this.baseUrl + '/beacon', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (response.ok) {
                this.log('Data sent via fetch');
            }
        } catch (error) {
            this.log('Fetch error:', error);
        }
    }
    
    getTimeOnPage() {
        if (!this.pageLoadTime) {
            this.pageLoadTime = Date.now();
        }
        return Date.now() - this.pageLoadTime;
    }
    
    setUserId(userId) {
        this.userId = userId;
    }
    
    log(...args) {
        if (this.debug) {
            console.log('[AnalyticsBeacon]', ...args);
        }
    }
}

// Global instance
if (typeof window !== 'undefined') {
    window.AnalyticsBeacon = AnalyticsBeacon;
    window.analytics = new AnalyticsBeacon();
}
