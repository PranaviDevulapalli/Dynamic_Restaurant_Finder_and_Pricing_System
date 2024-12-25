// static/js/app.js
let map;
let markers = [];

function initMap() {
    // First check if geolocation is available
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                
                initializeMapWithLocation(userLocation);
            },
            () => {
                // Fallback coordinates if geolocation fails
                initializeMapWithLocation({ lat: 20.5937, lng: 78.9629 });
            }
        );
    } else {
        initializeMapWithLocation({ lat: 20.5937, lng: 78.9629 });
    }
}

function initializeMapWithLocation(center) {
    map = new google.maps.Map(document.getElementById('map'), {
        center: center,
        zoom: 14,
        styles: [
            {
                featureType: "poi.business",
                stylers: [{ visibility: "off" }]
            }
        ]
    });

    map.addListener('click', handleMapClick);
    
    // Search for restaurants near the initial location
    fetchLocationDetails(center.lat, center.lng);
}

function handleMapClick(event) {
    clearMarkers();
    const clickedLocation = event.latLng;
    addMarker(clickedLocation);
    fetchLocationDetails(clickedLocation.lat(), clickedLocation.lng());
}

function clearMarkers() {
    markers.forEach(marker => marker.setMap(null));
    markers = [];
}

function addMarker(location, title = '') {
    const marker = new google.maps.Marker({
        position: location,
        map: map,
        animation: google.maps.Animation.DROP,
        title: title // Add title for hover text
    });
    
    // Add click listener to marker
    marker.addListener('click', () => {
        fetchLocationDetails(location.lat, location.lng);
        map.setCenter(location);
    });
    
    markers.push(marker);
    return marker;
}
function displayNoRestaurants() {
    const infoPanel = document.getElementById('info');
    infoPanel.innerHTML = `
        <div class="no-restaurants">
            <h3>No Restaurants Found</h3>
            <p>There are no restaurants available at this location.</p>
        </div>
    `;
}

function fetchLocationDetails(lat, lng) {
    const infoPanel = document.getElementById('info');
    infoPanel.innerHTML = '<div class="loading">Loading...</div>';

    // Add error handling and logging
    fetch(`/get-location-details/?lat=${lat}&lng=${lng}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data); // Debug log
            if (data.is_restaurant) {
                displayRestaurantDetails(data.restaurant_details);
            } else {
                if (data.nearby_restaurants && data.nearby_restaurants.length > 0) {
                    displayNearbyRestaurants(data.nearby_restaurants);
                } else {
                    displayNoRestaurants();
                }
            }
        })
        .catch(error => {
            console.error('Error fetching location details:', error);
            infoPanel.innerHTML = `
                <div class="error">
                    <h3>Error Loading Restaurants</h3>
                    <p>Unable to fetch restaurant details. Please try again later.</p>
                    <p>Technical details: ${error.message}</p>
                </div>
            `;
        });
}

// Rest of your existing functions remain the same...