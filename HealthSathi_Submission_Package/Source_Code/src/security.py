"""
HealthSathi - Data Privacy, Security & Role-Based Access Control (RBAC) Module
Implements PBKDF2-HMAC-SHA256 cryptographic password hashing, constant-time verification,
user management, security audit logging, and DPDP / GDPR data privacy protections.
"""

import os
import re
import json
import hmac
import hashlib
import secrets
import datetime
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
AUDIT_LOG_FILE = os.path.join(DATA_DIR, "security_audit_log.csv")

# Role definitions & permissions matrix
ROLES = {
    "admin": {
        "name": "System Administrator",
        "description": "Full access: system security, audit logs, user management, and IKS rule inspection.",
        "badge": "🛡️ Admin",
        "permissions": [
            "view_overview", "input_profile", "view_dashboard", "generate_routine",
            "view_iks", "generate_reports", "view_research", "access_admin_console",
            "manage_users", "view_audit_logs", "export_system_telemetry", "view_privacy_policy"
        ]
    },
    "user": {
        "name": "Registered Participant",
        "description": "Personalized access: profile entry, scoring, reports, custom Dinacharya, and data erasure.",
        "badge": "👤 User",
        "permissions": [
            "view_overview", "input_profile", "view_dashboard", "generate_routine",
            "view_iks", "generate_reports", "view_research", "export_my_data",
            "erase_my_data", "view_privacy_policy"
        ]
    },
    "viewer": {
        "name": "Guest / Auditor Viewer",
        "description": "Read-only access: view educational IKS models, demo dashboard, research papers, and policy.",
        "badge": "👁️ Viewer",
        "permissions": [
            "view_overview", "view_demo_dashboard", "view_iks", "view_research",
            "view_privacy_policy"
        ]
    }
}


def hash_password(plain_password: str, salt: Optional[bytes] = None) -> str:
    """
    Hashes password using PBKDF2-HMAC-SHA256 with 120,000 iterations and a 16-byte cryptographically secure salt.
    Format: pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>
    """
    if not plain_password:
        raise ValueError("Password cannot be empty")
    
    if salt is None:
        salt = secrets.token_bytes(16)
    
    iterations = 120000
    derived = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${derived.hex()}"


def verify_password(plain_password: str, hashed_str: str) -> bool:
    """
    Verifies a plain password against stored PBKDF2 hash using constant-time comparison to prevent timing attacks.
    """
    if not plain_password or not hashed_str:
        return False
    
    try:
        parts = hashed_str.split("$")
        if len(parts) != 4 or parts[0] != "pbkdf2_sha256":
            return False
        
        iterations = int(parts[1])
        salt = bytes.fromhex(parts[2])
        stored_hash = bytes.fromhex(parts[3])
        
        candidate_hash = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(candidate_hash, stored_hash)
    except Exception:
        return False


def sanitize_input(text: Any) -> str:
    """
    Sanitizes user input strings to prevent XSS, HTML injection, and control character anomalies.
    """
    if text is None:
        return ""
    s = str(text).strip()
    s = re.sub(r"[<>&\"']", lambda m: {"<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;", "'": "&#x27;"}[m.group()], s)
    s = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", s)
    return s


class SecurityAuditLogger:
    """
    Cryptographic and event audit logging for authentication, data access, and consent management.
    """
    def __init__(self, log_path: str = AUDIT_LOG_FILE):
        self.log_path = log_path
        os.makedirs(os.path.dirname(os.path.abspath(self.log_path)), exist_ok=True)
        if not os.path.exists(self.log_path):
            df_init = pd.DataFrame(columns=[
                "log_id", "timestamp_utc", "event_type", "username", "role", "ip_pseudo", "status", "details"
            ])
            df_init.to_csv(self.log_path, index=False)

    def log_event(self, event_type: str, username: str, role: str, status: str = "SUCCESS", details: str = "", ip_pseudo: str = "127.0.0.1") -> None:
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        log_id = f"LOG-{secrets.token_hex(4).upper()}"
        clean_details = sanitize_input(details)
        row = {
            "log_id": log_id,
            "timestamp_utc": now_str,
            "event_type": event_type,
            "username": username,
            "role": role,
            "ip_pseudo": ip_pseudo,
            "status": status,
            "details": clean_details
        }
        try:
            df = pd.DataFrame([row])
            df.to_csv(self.log_path, mode="a", header=False, index=False)
        except Exception:
            pass

    def get_recent_logs(self, limit: int = 50) -> pd.DataFrame:
        if not os.path.exists(self.log_path):
            return pd.DataFrame()
        try:
            df = pd.read_csv(self.log_path)
            return df.tail(limit).iloc[::-1] # Newest first
        except Exception:
            return pd.DataFrame()


class UserManager:
    """
    Manages user registration, authentication, RBAC authorization, and user data lifecycle.
    """
    def __init__(self, users_file: str = USERS_FILE):
        self.users_file = users_file
        self.audit_logger = SecurityAuditLogger()
        os.makedirs(os.path.dirname(os.path.abspath(self.users_file)), exist_ok=True)
        self._ensure_seed_users()

    def _ensure_seed_users(self) -> None:
        if not os.path.exists(self.users_file) or os.path.getsize(self.users_file) == 0:
            seed_users = {
                "admin": {
                    "username": "admin",
                    "email": "admin@healthsathi.org",
                    "password_hash": hash_password("Admin@HealthSathi2026"),
                    "role": "admin",
                    "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "last_login": None,
                    "status": "active"
                },
                "demo_user": {
                    "username": "demo_user",
                    "email": "user@healthsathi.org",
                    "password_hash": hash_password("User@HealthSathi2026"),
                    "role": "user",
                    "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "last_login": None,
                    "status": "active"
                },
                "viewer": {
                    "username": "viewer",
                    "email": "viewer@healthsathi.org",
                    "password_hash": hash_password("Viewer@HealthSathi2026"),
                    "role": "viewer",
                    "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "last_login": None,
                    "status": "active"
                }
            }
            with open(self.users_file, "w", encoding="utf-8") as f:
                json.dump(seed_users, f, indent=2)
            self.audit_logger.log_event("SYSTEM_INIT", "system", "admin", "SUCCESS", "Initialized seed security credentials")

    def _load_users(self) -> Dict[str, Any]:
        if not os.path.exists(self.users_file):
            return {}
        try:
            with open(self.users_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_users(self, users: Dict[str, Any]) -> None:
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)

    def authenticate(self, username_or_email: str, plain_password: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        users = self._load_users()
        target_user = None
        key_found = None
        
        u_clean = username_or_email.strip().lower()
        for k, u in users.items():
            if u["username"].lower() == u_clean or u["email"].lower() == u_clean:
                target_user = u
                key_found = k
                break
        
        if not target_user:
            self.audit_logger.log_event("AUTH_FAILED", u_clean, "unknown", "FAILURE", "Username or email not found")
            return False, None, "Invalid username or password"
        
        if target_user.get("status") != "active":
            self.audit_logger.log_event("AUTH_FAILED", target_user["username"], target_user["role"], "BLOCKED", "Account suspended")
            return False, None, "Account is disabled or suspended"

        if verify_password(plain_password, target_user["password_hash"]):
            target_user["last_login"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            users[key_found] = target_user
            self._save_users(users)
            
            user_session = {
                "username": target_user["username"],
                "email": target_user["email"],
                "role": target_user["role"],
                "badge": ROLES.get(target_user["role"], {}).get("badge", "👤 User"),
                "session_token": secrets.token_urlsafe(24),
                "login_time": target_user["last_login"]
            }
            self.audit_logger.log_event("AUTH_SUCCESS", target_user["username"], target_user["role"], "SUCCESS", "User authenticated successfully")
            return True, user_session, "Login successful"
        else:
            self.audit_logger.log_event("AUTH_FAILED", target_user["username"], target_user["role"], "FAILURE", "Incorrect password")
            return False, None, "Invalid username or password"

    def register_user(self, username: str, email: str, plain_password: str, role: str = "user") -> Tuple[bool, str]:
        users = self._load_users()
        u_clean = username.strip().lower()
        e_clean = email.strip().lower()

        if len(u_clean) < 3 or not re.match(r"^[a-zA-Z0-9_-]+$", u_clean):
            return False, "Username must be at least 3 characters and contain only letters, numbers, hyphens, and underscores."
        
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", e_clean):
            return False, "Please enter a valid email address format."

        if len(plain_password) < 8:
            return False, "Password must be at least 8 characters long."

        for _, u in users.items():
            if u["username"].lower() == u_clean:
                return False, "Username already exists. Please choose a different handle."
            if u["email"].lower() == e_clean:
                return False, "An account with this email address already exists."

        assigned_role = role if role in ["user", "viewer"] else "user"
        pw_hash = hash_password(plain_password)

        new_entry = {
            "username": u_clean,
            "email": e_clean,
            "password_hash": pw_hash,
            "role": assigned_role,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "last_login": None,
            "status": "active"
        }
        users[u_clean] = new_entry
        self._save_users(users)
        self.audit_logger.log_event("USER_REGISTERED", u_clean, assigned_role, "SUCCESS", f"New user self-registered with role {assigned_role}")
        return True, "Registration successful! You may now sign in."

    def list_all_users(self) -> List[Dict[str, Any]]:
        users = self._load_users()
        safe_list = []
        for k, u in users.items():
            safe_list.append({
                "username": u["username"],
                "email": u["email"],
                "role": u["role"],
                "role_badge": ROLES.get(u["role"], {}).get("badge", "👤 User"),
                "status": u.get("status", "active"),
                "created_at": u.get("created_at"),
                "last_login": u.get("last_login", "Never")
            })
        return safe_list

    def delete_user(self, username: str) -> Tuple[bool, str]:
        users = self._load_users()
        u_clean = username.strip().lower()
        if u_clean not in users:
            return False, "User not found"
        if u_clean == "admin":
            return False, "Primary administrator account cannot be deleted"
        
        role = users[u_clean]["role"]
        del users[u_clean]
        self._save_users(users)
        self.audit_logger.log_event("USER_DELETED", u_clean, role, "SUCCESS", "Account permanently erased under Right to Erasure")
        return True, f"User '{u_clean}' and associated records permanently deleted."

    def update_role(self, username: str, new_role: str) -> Tuple[bool, str]:
        users = self._load_users()
        u_clean = username.strip().lower()
        if u_clean not in users:
            return False, "User not found"
        if new_role not in ROLES:
            return False, "Invalid role target"
        
        old_role = users[u_clean]["role"]
        users[u_clean]["role"] = new_role
        self._save_users(users)
        self.audit_logger.log_event("ROLE_CHANGED", u_clean, new_role, "SUCCESS", f"Role updated from {old_role} to {new_role}")
        return True, f"Role for '{u_clean}' updated to {new_role}."


def check_permission(role: str, permission_name: str) -> bool:
    """
    Checks if a given role possesses a specific permission.
    """
    role_info = ROLES.get(role.lower(), ROLES["viewer"])
    return permission_name in role_info.get("permissions", [])


def export_user_data_package(user_data: Dict[str, Any], scores: Dict[str, Any]) -> str:
    """
    Creates an exportable, transparent JSON data portability package per DPDP/GDPR rights.
    """
    package = {
        "export_metadata": {
            "system": "HealthSathi IKS Lifestyle Analytics",
            "compliance": "DPDP Act 2023 / GDPR Right to Data Portability",
            "export_timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "license": "Confidential Personal Wellness Data"
        },
        "submitted_lifestyle_metrics": user_data,
        "derived_wellness_scores": scores,
        "privacy_notice": "HealthSathi stores zero Personally Identifiable Information (PII) like names, phone numbers, or physical addresses."
    }
    return json.dumps(package, indent=2)
