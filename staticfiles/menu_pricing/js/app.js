// static/js/app.js
let map;
let markers = [];

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 20.5937, lng: 78.9629 },
        zoom: 12,
        styles: [
            {
                featureType: "poi.business",
                stylers: [{ visibility: "off" }]
            }
        ]
    });

    map.addListener('click', handleMapClick);
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

function addMarker(location) {
    const marker = new google.maps.Marker({
        position: location,
        map: map,
        animation: google.maps.Animation.DROP
    });
    markers.push(marker);
}

function fetchLocationDetails(lat, lng) {
    const infoPanel = document.getElementById('info');
    infoPanel.innerHTML = '<div class="loading">Loading...</div>';

    fetch(`/get-location-details/?lat=${lat}&lng=${lng}`)
        .then(response => response.json())
        .then(data => {
            if (data.is_restaurant) {
                displayRestaurantDetails(data.restaurant_details);
            } else {
                if (data.nearby_restaurants) {
                    displayNearbyRestaurants(data.nearby_restaurants);
                } else {
                    displayNoRestaurants();
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            infoPanel.innerHTML = '<div class="error">Failed to fetch restaurant details.</div>';
        });
}

function displayRestaurantDetails(details) {
    const infoPanel = document.getElementById('info');
    const statusClass = details.status.toLowerCase() === 'open' ? 'status-open' : 'status-closed';

    infoPanel.innerHTML = `
        <h2>${details.name}</h2>
        <p class="address">${details.address}</p>
        
        <div class="weather-info">
            <p><strong>Temperature:</strong> ${details.weather.temperature.toFixed(1)}°C</p>
            <p><strong>Weather:</strong> ${details.weather.rain_chance}</p>
        </div>

        <div class="busyness-indicator">
            <span>Busyness:</span>
            <div class="busyness-bar">
                <div class="busyness-fill" style="width: ${details.busyness}%"></div>
            </div>
            <span>${details.busyness}%</span>
        </div>

        <span class="status-badge ${statusClass}">${details.status}</span>

        <h3>Menu Items</h3>
        <div class="menu-items">
            ${details.menu_items.map(item => `
                <div class="menu-item">
                    <span>${item.name}</span>
                    <span class="price">$${item.price.toFixed(2)}</span>
                </div>
            `).join('')}
        </div>
    `;
}

function displayNearbyRestaurants(restaurants) {
    const infoPanel = document.getElementById('info');
    
    infoPanel.innerHTML = `
        <h2>Nearby Restaurants (within 5km)</h2>
        <ul class="restaurant-list">
            ${restaurants.map(restaurant => `
                <li class="restaurant-item" 
                    onclick="handleRestaurantClick(${restaurant.lat}, ${restaurant.lng})"
                    onmouseover="highlightMarker(${restaurant.lat}, ${restaurant.lng})"
                    onmouseout="unhighlightMarker()">
                    <strong>${restaurant.name}</strong>
                    <p>${restaurant.vicinity}</p>
                </li>
            `).join('')}
        </ul>
    `;

    restaurants.forEach(restaurant => {
        addMarker({ lat: restaurant.lat, lng: restaurant.lng });
    });
}

function displayNoRestaurants() {
    const infoPanel = document.getElementById('info');
    infoPanel.innerHTML = `
        <div class="no-results">
            <h2>No Restaurants Found</h2>
            <p>There are no restaurants available within 5km radius of the selected location.</p>
        </div>
    `;
}

function handleRestaurantClick(lat, lng) {
    clearMarkers();
    addMarker({ lat, lng });
    map.setCenter({ lat, lng });
    map.setZoom(15);
    fetchLocationDetails(lat, lng);
}

function highlightMarker(lat, lng) {
    markers.forEach(marker => {
        if (marker.getPosition().lat() === lat && marker.getPosition().lng() === lng) {
            marker.setAnimation(google.maps.Animation.BOUNCE);
        }
    });
}

function unhighlightMarker() {
    markers.forEach(marker => {
        marker.setAnimation(null);
    });
}