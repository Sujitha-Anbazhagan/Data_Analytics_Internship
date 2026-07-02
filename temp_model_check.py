import os, sys
sys.path.insert(0, os.path.abspath('.'))
from src.predict import load_model
BASE_DIR = os.path.abspath('.')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'churn_rf_model.pkl')
print('model path:', MODEL_PATH)
try:
    model = load_model(MODEL_PATH)
    print('loaded model type:', type(model))
    print('has feature_names_in_:', hasattr(model, 'feature_names_in_'))
    if hasattr(model, 'feature_names_in_'):
        print('feature_names sample:', list(model.feature_names_in_)[:20])
    else:
        print('feature_names_in_ is missing')
except Exception as e:
    import traceback
    traceback.print_exc()
