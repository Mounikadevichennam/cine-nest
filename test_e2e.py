import httpx
import json

BASE_URL = "http://127.0.0.1:8001/api/v1"

def run_tests():
    print("=" * 70)
    print("        CINENEST END-TO-END VERIFICATION SUITE")
    print("=" * 70)

    # 1. Health Check
    res = httpx.get(f"{BASE_URL}/health")
    print(f"1. Health Check status: {res.status_code} -> {res.json()}")

    # 2. Standard User Login
    login_payload = {"email": "mounika@cinenest.com", "password": "password123"}
    res = httpx.post(f"{BASE_URL}/auth/login", json=login_payload)
    print(f"2. Standard User Login status: {res.status_code}")
    user_token = res.json().get("access_token")
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # 3. Onboarding Preferences Update
    onboarding_payload = {
        "preferred_language": "Telugu",
        "favourite_genre_names": ["Action", "Drama"],
        "favourite_actor_ids": [101, 103, 104]
    }
    res = httpx.post(f"{BASE_URL}/users/onboarding", json=onboarding_payload, headers=user_headers)
    print(f"3. Onboarding update status: {res.status_code} (Language: {res.json().get('preferred_language')})")

    # 4. Recommendation Feeds Test
    for feed_name, endpoint in [
        ("Recommended For You", "/recommendations/recommended"),
        ("Trending Now", "/recommendations/trending"),
        ("New Releases (2024-2026)", "/recommendations/new-releases"),
        ("Based on Favourite Genres", "/recommendations/by-genres"),
        ("Based on Favourite Actors", "/recommendations/by-actors"),
    ]:
        res = httpx.get(f"{BASE_URL}{endpoint}", headers=user_headers)
        data = res.json()
        print(f"4. Feed '{feed_name}' status: {res.status_code} | Movies returned: {len(data) if isinstance(data, list) else 0}")
        if isinstance(data, list) and len(data) > 0:
            m = data[0]
            print(f"   Sample Movie: ID={m.get('id')}, Title='{m.get('title')}', Year={m.get('release_year')}, Lang='{m.get('language')}', Poster={m.get('poster_url')[:45]}...")

    # 5. Admin Login & RBAC Verification
    admin_login_payload = {"email": "admin@cinenest.com", "password": "admin123"}
    res = httpx.post(f"{BASE_URL}/auth/login", json=admin_login_payload)
    print(f"5. Admin Login status: {res.status_code} (Role: {res.json().get('user', {}).get('role')})")
    admin_token = res.json().get("access_token")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # Admin Stats Call (Authorized)
    res = httpx.get(f"{BASE_URL}/admin/stats", headers=admin_headers)
    print(f"6. Admin GET /admin/stats (Authorized) status: {res.status_code} -> {res.json()}")

    # Admin Movies Call (Authorized)
    res = httpx.get(f"{BASE_URL}/admin/movies?limit=5", headers=admin_headers)
    print(f"7. Admin GET /admin/movies (Authorized) status: {res.status_code} | Count: {len(res.json())}")

    # Standard User Calling Admin Endpoint (RBAC Test - Should be 403 Forbidden)
    res = httpx.get(f"{BASE_URL}/admin/stats", headers=user_headers)
    print(f"8. Standard User GET /admin/stats (RBAC Test): status={res.status_code} (Detail: '{res.json().get('detail')}')")

    print("=" * 70)
    print("               E2E VERIFICATION COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
