/**
 * HBnB Web Client - Places Functions
 * Handles loading and displaying places
 */

// Store all places for filtering
let allPlaces = [];

/**
 * Load all places
 */
async function loadPlaces() {
    const loading = document.getElementById('loading');
    const placesList = document.getElementById('places-list');
    const placesContainer = document.getElementById('placesContainer'); // For backward compatibility
    const emptyState = document.getElementById('emptyState');

    // Use places-list (Task 2 requirement) or fallback to placesContainer
    const container = placesList || placesContainer;
    if (!container) return;

    try {
        if (loading) loading.classList.remove('hidden');
        container.innerHTML = '';
        if (emptyState) emptyState.classList.add('hidden');

        const places = await apiRequest('/places/');
        allPlaces = places;

        if (loading) loading.classList.add('hidden');

        if (places.length === 0) {
            if (emptyState) emptyState.classList.remove('hidden');
            return;
        }

        // Display places
        displayPlaces(places);
    } catch (error) {
        if (loading) loading.classList.add('hidden');
        container.innerHTML = `
            <div class="empty-state">
                <h3>Error Loading Places</h3>
                <p>${error.message || 'Failed to load places. Please try again later.'}</p>
            </div>
        `;
        console.error('Error loading places:', error);
    }
}

/**
 * Filter places by price (Task 2 requirement)
 */
function filterPlacesByPrice() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    const selectedPrice = priceFilter.value;

    if (selectedPrice === 'all') {
        displayPlaces(allPlaces);
        return;
    }

    const maxPrice = parseFloat(selectedPrice);
    const filteredPlaces = allPlaces.filter(place => place.price <= maxPrice);
    displayPlaces(filteredPlaces);
}

/**
 * Display places in the container (Task 2 requirement)
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    const placesContainer = document.getElementById('placesContainer'); // For backward compatibility
    const emptyState = document.getElementById('emptyState');

    // Use places-list (Task 2 requirement) or fallback to placesContainer
    const container = placesList || placesContainer;
    if (!container) return;

    if (places.length === 0) {
        if (emptyState) emptyState.classList.remove('hidden');
        container.innerHTML = '';
        return;
    }

    if (emptyState) emptyState.classList.add('hidden');
    
    // Pre-defined hotel image URLs from Unsplash (actual hotel photos)
    const hotelImageUrls = [
        'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&h=300&fit=crop&q=80', // Hotel room
        'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=400&h=300&fit=crop&q=80', // Luxury hotel
        'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400&h=300&fit=crop&q=80', // Resort
        'https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=400&h=300&fit=crop&q=80', // Apartment
        'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400&h=300&fit=crop&q=80', // Villa
        'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop&q=80', // Mountain lodge
        'https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=400&h=300&fit=crop&q=80', // Penthouse
        'https://images.unsplash.com/photo-1556912172-45b7abe8b7e4?w=400&h=300&fit=crop&q=80', // Boutique hotel
        'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=400&h=300&fit=crop&q=80', // Modern apartment
        'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&h=300&fit=crop&q=80', // Beach resort
        'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=400&h=300&fit=crop&q=80', // Hotel interior
        'https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=400&h=300&fit=crop&q=80', // Luxury suite
        'https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=400&h=300&fit=crop&q=80', // Resort pool
        'https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=400&h=300&fit=crop&q=80', // Apartment interior
        'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400&h=300&fit=crop&q=80', // Villa exterior
    ];
    
    container.innerHTML = places.map((place, index) => {
        // Use predefined hotel images, cycling through them
        const imageUrl = hotelImageUrls[index % hotelImageUrls.length];
        
        // Create unique image URL with cache busting
        const uniqueImageUrl = `${imageUrl}&sig=${place.id.substring(0, 8)}`;
        
        return `
        <div class="place-card scroll-reveal">
            <div class="place-card-image" data-place-id="${place.id}">
                <img src="${uniqueImageUrl}" 
                     alt="${escapeHtml(place.name)}" 
                     loading="lazy"
                     crossorigin="anonymous"
                     onerror="handlePlaceImageError(this, '${place.id}');">
                <div class="place-card-image-fallback" id="fallback-${place.id}" style="display: none;">
                    🏨 ${place.name.charAt(0).toUpperCase()}
                </div>
            </div>
            <div class="place-card-content">
                <h3 class="place-card-title">${escapeHtml(place.name)}</h3>
                <div class="place-card-price">${formatPrice(place.price)}</div>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            </div>
        </div>
        `;
    }).join('');
    
    // Add scroll reveal classes to new cards
    setTimeout(() => {
        container.querySelectorAll('.place-card').forEach((card, index) => {
            card.classList.add('scroll-reveal');
            card.style.animationDelay = `${index * 0.1}s`;
        });
        if (typeof initScrollReveal === 'function') {
            initScrollReveal();
        }
    }, 100);
    
    // Add global error handler for place images
    if (typeof window.handlePlaceImageError === 'undefined') {
        window.handlePlaceImageError = function(img, placeId) {
            // Try fallback image from different source
            const fallbackIndex = parseInt(placeId.substring(0, 2), 16) % hotelImageUrls.length;
            const fallbackUrl = hotelImageUrls[fallbackIndex] + '&sig=' + placeId.substring(0, 8);
            
            if (img.src !== fallbackUrl) {
                img.src = fallbackUrl;
                img.onerror = function() {
                    // If fallback also fails, show gradient fallback
                    this.style.display = 'none';
                    const fallback = document.getElementById('fallback-' + placeId);
                    if (fallback) {
                        fallback.style.display = 'flex';
                    }
                };
            } else {
                // Both failed, show gradient
                img.style.display = 'none';
                const fallback = document.getElementById('fallback-' + placeId);
                if (fallback) {
                    fallback.style.display = 'flex';
                }
            }
        };
    }
}

/**
 * Delete a place (Admin only)
 */
async function deletePlace(placeId) {
    if (!confirm('Are you sure you want to delete this place? This action cannot be undone.')) {
        return;
    }

    try {
        await apiRequest(`/places/${placeId}`, {
            method: 'DELETE',
        });

        alert('Place deleted successfully!');
        window.location.href = 'index.html';
    } catch (error) {
        alert('Error deleting place: ' + (error.message || 'Unknown error'));
        console.error('Error deleting place:', error);
    }
}

/**
 * Load place details
 */
async function loadPlaceDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (!placeId) {
        const loading = document.getElementById('loading');
        if (loading) {
            loading.innerHTML = `
                <div class="empty-state">
                    <h3>No Place Selected</h3>
                    <p>Please select a place from the <a href="index.html">places list</a>.</p>
                </div>
            `;
        }
        return;
    }

    const loading = document.getElementById('loading');
    const placeDetails = document.getElementById('place-details'); // Task 3 requirement
    const placeDetailsAlt = document.getElementById('placeDetails'); // For backward compatibility
    const targetPlaceDetails = placeDetails || placeDetailsAlt;
    const reviewsSection = document.getElementById('reviewsSection');

    try {
        loading.classList.remove('hidden');
        if (targetPlaceDetails) targetPlaceDetails.classList.add('hidden');

        // Load place details
        const place = await apiRequest(`/places/${placeId}`);

        // Load owner information
        let ownerName = 'Unknown';
        try {
            const owner = await apiRequest(`/users/${place.owner_id}`);
            ownerName = `${owner.first_name} ${owner.last_name}`;
        } catch (error) {
            console.error('Error loading owner:', error);
        }

        // Load amenities
        const amenitiesList = document.getElementById('placeAmenities');
        if (amenitiesList && place.amenity_ids && place.amenity_ids.length > 0) {
            try {
                const amenities = await Promise.all(
                    place.amenity_ids.map(id => apiRequest(`/amenities/${id}`))
                );
                amenitiesList.innerHTML = amenities.map(amenity => 
                    `<span class="amenity-tag">${escapeHtml(amenity.name)}</span>`
                ).join('');
            } catch (error) {
                console.error('Error loading amenities:', error);
                amenitiesList.innerHTML = '<p>Unable to load amenities</p>';
            }
        } else if (amenitiesList) {
            amenitiesList.innerHTML = '<p>No amenities listed</p>';
        }

        // Populate place details
        document.getElementById('placeName').textContent = place.name;
        document.getElementById('placePrice').textContent = formatPrice(place.price);
        document.getElementById('placeDescription').textContent = place.description;
        document.getElementById('placeHost').textContent = ownerName;
        document.getElementById('placeLocation').textContent = 
            `Lat: ${place.latitude.toFixed(4)}, Lng: ${place.longitude.toFixed(4)}`;

        loading.classList.add('hidden');
        if (targetPlaceDetails) targetPlaceDetails.classList.remove('hidden');

        // Show admin actions ONLY if user is admin
        const placeAdminActions = document.getElementById('placeAdminActions');
        const userIsAdmin = isAdmin();
        
        if (placeAdminActions) {
            if (userIsAdmin) {
                placeAdminActions.classList.remove('hidden');
                placeAdminActions.style.display = 'flex';
                // Add delete button event listener
                const deleteButton = document.getElementById('deletePlaceButton');
                if (deleteButton) {
                    deleteButton.onclick = () => deletePlace(placeId);
                }
            } else {
                placeAdminActions.classList.add('hidden');
                placeAdminActions.style.display = 'none';
            }
        }

        // Load reviews
        await loadReviews(placeId);

        // Check if current user is the place owner - hide add review form if they are
        const addReviewSection = document.getElementById('add-review'); // Task 3 requirement
        const addReviewSectionAlt = document.getElementById('addReviewSection'); // For backward compatibility
        const targetAddReview = addReviewSection || addReviewSectionAlt;
        // Check if current user is the place owner - verify from database
        const currentUserInfo = getCurrentUserInfo();
        const currentUserId = currentUserInfo ? currentUserInfo.user_id : null;
        
        // Verify place ownership from database (place.owner_id comes from API)
        const isPlaceOwner = currentUserId && place.owner_id && place.owner_id === currentUserId;

        if (targetAddReview) {
            if (isPlaceOwner) {
                // User owns this place - hide the add review form
                targetAddReview.style.display = 'none';
                targetAddReview.classList.add('hidden');
                // Show a message instead
                if (!document.getElementById('ownerCannotReviewMessage')) {
                    const messageDiv = document.createElement('div');
                    messageDiv.id = 'ownerCannotReviewMessage';
                    messageDiv.className = 'add-review';
                    messageDiv.style.cssText = 'text-align: center; padding: 2rem; color: var(--text-secondary); background: var(--bg-tertiary); border-radius: var(--border-radius); margin-top: 2rem;';
                    messageDiv.innerHTML = `
                        <h3 style="margin-bottom: 0.5rem; color: var(--text-primary);">Cannot Review Your Own Place</h3>
                        <p>As the owner of this place, you cannot add a review to your own listing.</p>
                    `;
                    targetAddReview.parentNode.insertBefore(messageDiv, targetAddReview.nextSibling);
                }
            } else if (isAuthenticated()) {
                // User is authenticated and not the owner - show add review form
                targetAddReview.style.display = 'block';
                targetAddReview.classList.remove('hidden');
                // Store place ID for the form
                targetAddReview.dataset.placeId = placeId;
                // Hide the message if it exists
                const messageDiv = document.getElementById('ownerCannotReviewMessage');
                if (messageDiv) {
                    messageDiv.remove();
                }
            } else {
                // User is not authenticated - hide add review form
                targetAddReview.style.display = 'none';
                targetAddReview.classList.add('hidden');
            }
        }
    } catch (error) {
        loading.innerHTML = `
            <div class="empty-state">
                <h3>Error Loading Place</h3>
                <p>${error.message || 'Failed to load place details. Please try again later.'}</p>
                <a href="index.html" class="details-button" style="margin-top: 1rem;">Back to Places</a>
            </div>
        `;
        console.error('Error loading place details:', error);
    }
}
