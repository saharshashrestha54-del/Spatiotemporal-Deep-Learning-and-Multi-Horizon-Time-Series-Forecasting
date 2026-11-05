import numpy as np

def compute_continuous_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)

    mask = ~np.isnan(y_true) & ~np.isnan(y_pred)
    y_t = y_true[mask]
    y_p = y_pred[mask]

    rmse = np.sqrt(np.mean((y_p - y_t) ** 2))
    mae = np.mean(np.abs(y_p - y_t))

    r = np.corrcoef(y_t, y_p)[0, 1] if len(y_t) > 1 else 0.0

    sigma_sim = np.std(y_p)
    sigma_obs = np.std(y_t)
    mu_sim = np.mean(y_p)
    mu_obs = np.mean(y_t)

    alpha = (sigma_sim / sigma_obs) if sigma_obs > 0 else 1.0
    beta = (mu_sim / mu_obs) if mu_obs > 0 else 1.0

    kge = 1.0 - np.sqrt((r - 1.0) ** 2 + (alpha - 1.0) ** 2 + (beta - 1.0) ** 2)

    return {
        "RMSE": float(rmse),
        "MAE": float(mae),
        "Pearson_r": float(r),
        "KGE": float(kge)
    }

def compute_contingency_metrics(y_true_binary: np.ndarray, y_pred_binary: np.ndarray) -> dict:
    
    y_true = np.asarray(y_true_binary, dtype=int)
    y_pred = np.asarray(y_pred_binary, dtype=int)

    hits = np.sum((y_true == 1) & (y_pred == 1))
    misses = np.sum((y_true == 1) & (y_pred == 0))
    false_alarms = np.sum((y_true == 0) & (y_pred == 1))
    correct_negatives = np.sum((y_true == 0) & (y_pred == 0))

    pod = hits / (hits + misses) if (hits + misses) > 0 else 0.0
    far = false_alarms / (hits + false_alarms) if (hits + false_alarms) > 0 else 0.0
    csi = hits / (hits + misses + false_alarms) if (hits + misses + false_alarms) > 0 else 0.0

    return {
        "POD": float(pod),
        "FAR": float(far),
        "CSI": float(csi),
        "Hits": int(hits),
        "Misses": int(misses),
        "False_Alarms": int(false_alarms)
    }
