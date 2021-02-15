from rest_framework.throttling import UserRateThrottle

class SimpleUserRateThrottle(UserRateThrottle):
    scope = 'user'
    
    def throttle_success(self):
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)

        print(self.history)
        print(self.cache)
        return True

class CustomerRateThrottle(UserRateThrottle):
    scope = 'customer'