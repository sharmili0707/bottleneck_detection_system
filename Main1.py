
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import webbrowser
from datetime import datetime
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import warnings

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

class SupplyChainGUI:
    """GUI Application for Supply Chain Bottleneck Detection"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI-Based Supply Chain Bottleneck Detection System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
      
        self.system = None
        self.results = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the GUI interface"""
        
       
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🚚 AI-Based Supply Chain Bottleneck Detection System",
                              font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=20)
        
    
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
    
        left_panel = tk.Frame(main_frame, bg='white', relief='ridge', bd=2)
        left_panel.pack(side='left', fill='y', padx=(0, 10), ipadx=10, ipady=10)
        
       
        right_panel = tk.Frame(main_frame, bg='white', relief='ridge', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, ipadx=10, ipady=10)
        
      
        tk.Label(left_panel, text="📊 System Controls", font=('Arial', 14, 'bold'),
                bg='white').pack(pady=10)
        
    
        tk.Label(left_panel, text="Dataset Path:", font=('Arial', 10, 'bold'),
                bg='white').pack(anchor='w', pady=(10, 0))
        
        self.path_label = tk.Label(left_panel, 
                                   text=r"C:\Users\SHARMILI\Desktop\FINAL CODE\DATASET\supply_chain_data.csv",
                                   bg='white', fg='blue', wraplength=250,
                                   font=('Arial', 8))
        self.path_label.pack(anchor='w', pady=(0, 10))
        

        self.run_btn = tk.Button(left_panel, text="▶ Run Analysis", 
                                 command=self.run_analysis,
                                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                                 padx=20, pady=10, cursor='hand2')
        self.run_btn.pack(pady=10, fill='x')
        
        self.view_dashboard_btn = tk.Button(left_panel, text="📊 View Dashboard", 
                                           command=self.view_dashboard,
                                           bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                                           padx=20, pady=10, cursor='hand2',
                                           state='disabled')
        self.view_dashboard_btn.pack(pady=5, fill='x')
        
        self.view_report_btn = tk.Button(left_panel, text="📄 View Report", 
                                        command=self.view_report,
                                        bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                                        padx=20, pady=10, cursor='hand2',
                                        state='disabled')
        self.view_report_btn.pack(pady=5, fill='x')
        
   
        tk.Label(left_panel, text="Status:", font=('Arial', 10, 'bold'),
                bg='white').pack(anchor='w', pady=(20, 0))
        self.status_label = tk.Label(left_panel, text="Ready", bg='white', fg='green')
        self.status_label.pack(anchor='w')
        

        metrics_frame = tk.LabelFrame(left_panel, text="📈 Key Metrics", 
                                      bg='white', font=('Arial', 10, 'bold'))
        metrics_frame.pack(fill='x', pady=20)
        
        self.metrics_labels = {}
        metrics = ['Total Records', 'Delay Rate', 'Accuracy', 'Bottlenecks']
        for metric in metrics:
            frame = tk.Frame(metrics_frame, bg='white')
            frame.pack(fill='x', pady=5)
            tk.Label(frame, text=f"{metric}:", bg='white', 
                    font=('Arial', 10)).pack(side='left')
            self.metrics_labels[metric] = tk.Label(frame, text="--", bg='white', 
                                                   font=('Arial', 10, 'bold'), fg='blue')
            self.metrics_labels[metric].pack(side='right')
        
     
        tk.Label(right_panel, text="📋 Analysis Results", font=('Arial', 14, 'bold'),
                bg='white').pack(pady=10)
        
      
        notebook = ttk.Notebook(right_panel)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
   
        console_tab = tk.Frame(notebook, bg='white')
        notebook.add(console_tab, text="Console Output")
        
        self.console_output = scrolledtext.ScrolledText(console_tab, wrap=tk.WORD,
                                                        width=60, height=25,
                                                        font=('Consolas', 9))
        self.console_output.pack(fill='both', expand=True, padx=5, pady=5)
        
    
        bottlenecks_tab = tk.Frame(notebook, bg='white')
        notebook.add(bottlenecks_tab, text="🔍 Bottlenecks")
        
        self.bottlenecks_tree = ttk.Treeview(bottlenecks_tab, 
                                             columns=('Feature', 'Importance', 'Type', 'Severity'),
                                             show='headings', height=15)
        self.bottlenecks_tree.heading('Feature', text='Feature')
        self.bottlenecks_tree.heading('Importance', text='Importance')
        self.bottlenecks_tree.heading('Type', text='Type')
        self.bottlenecks_tree.heading('Severity', text='Severity')
        self.bottlenecks_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
     
        suppliers_tab = tk.Frame(notebook, bg='white')
        notebook.add(suppliers_tab, text="🏭 Suppliers")
        
        self.suppliers_tree = ttk.Treeview(suppliers_tab, 
                                          columns=('Supplier', 'Delay Rate', 'Lead Time', 'Defect Rate'),
                                          show='headings', height=15)
        self.suppliers_tree.heading('Supplier', text='Supplier')
        self.suppliers_tree.heading('Delay Rate', text='Delay Rate')
        self.suppliers_tree.heading('Lead Time', text='Lead Time')
        self.suppliers_tree.heading('Defect Rate', text='Defect Rate')
        self.suppliers_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
     
        products_tab = tk.Frame(notebook, bg='white')
        notebook.add(products_tab, text="📦 Products")
        
        self.products_tree = ttk.Treeview(products_tab, 
                                         columns=('Product', 'Delay Rate', 'Defect Rate', 'Shipping Time'),
                                         show='headings', height=15)
        self.products_tree.heading('Product', text='Product')
        self.products_tree.heading('Delay Rate', text='Delay Rate')
        self.products_tree.heading('Defect Rate', text='Defect Rate')
        self.products_tree.heading('Shipping Time', text='Shipping Time')
        self.products_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
       
        recommendations_tab = tk.Frame(notebook, bg='white')
        notebook.add(recommendations_tab, text="💡 Recommendations")
        
        self.recommendations_text = scrolledtext.ScrolledText(recommendations_tab, 
                                                              wrap=tk.WORD,
                                                              width=60, height=25,
                                                              font=('Arial', 10))
        self.recommendations_text.pack(fill='both', expand=True, padx=5, pady=5)
        
      
        self.progress = ttk.Progressbar(left_panel, mode='indeterminate')
        self.progress.pack(fill='x', pady=10)
        
    def log_console(self, message):
        """Add message to console output"""
        self.console_output.insert(tk.END, message + "\n")
        self.console_output.see(tk.END)
        self.root.update_idletasks()
    
    def run_analysis(self):
        """Run the analysis in a separate thread"""
        self.run_btn.config(state='disabled')
        self.progress.start()
        self.status_label.config(text="Running analysis...", fg='orange')
        self.log_console("="*60)
        self.log_console("Starting Supply Chain Analysis...")
        self.log_console("="*60)
        
      
        thread = threading.Thread(target=self._run_analysis_thread)
        thread.start()
    
    def _run_analysis_thread(self):
        """Thread function to run analysis"""
        try:
            CSV_PATH = r"C:\Users\SHARMILI\Desktop\FINAL CODE\DATASET\supply_chain_data.csv"
            
           
            import sys
            from io import StringIO
            
         
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
      
            self.system = SupplyChainBottleneckSystem(CSV_PATH)
            self.results = self.system.run_complete_analysis()
           
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
      
            for line in output.split('\n'):
                self.log_console(line)
            
       
            self.root.after(0, self.update_metrics)
            
     
            self.root.after(0, self.update_bottlenecks_table)
            
    
            if self.results['supplier_performance'] is not None:
                self.root.after(0, self.update_suppliers_table)
            
         
            if self.results['product_analysis'] is not None:
                self.root.after(0, self.update_products_table)
            
         
            self.root.after(0, self.update_recommendations)
            
       
            self.root.after(0, self.enable_buttons)
            
            self.root.after(0, lambda: self.status_label.config(text="Analysis Complete!", fg='green'))
            
        except Exception as e:
            self.root.after(0, lambda: self.log_console(f"❌ Error: {str(e)}"))
            self.root.after(0, lambda: self.status_label.config(text="Error occurred", fg='red'))
            self.root.after(0, lambda: self.run_btn.config(state='normal'))
            self.progress.stop()
    
    def update_metrics(self):
        """Update metrics display"""
        if self.results:
            self.metrics_labels['Total Records'].config(
                text=str(self.results['report']['dataset_info']['total_records']))
            self.metrics_labels['Delay Rate'].config(
                text=f"{self.results['report']['dataset_info']['delay_rate']:.1f}%")
            self.metrics_labels['Accuracy'].config(
                text=f"{self.results['model_accuracy']:.1%}")
            self.metrics_labels['Bottlenecks'].config(
                text=str(len(self.results['bottlenecks'])))
    
    def update_bottlenecks_table(self):
        """Update bottlenecks table"""
      
        for item in self.bottlenecks_tree.get_children():
            self.bottlenecks_tree.delete(item)
        
  
        for b in self.results['bottlenecks'][:20]:
            self.bottlenecks_tree.insert('', 'end', values=(
                b['feature'][:30],
                f"{b['importance']:.2%}",
                b['bottleneck_type'],
                b['severity']
            ))
    
    def update_suppliers_table(self):
        """Update suppliers table"""
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
        
        for _, row in self.results['supplier_performance'].iterrows():
            self.suppliers_tree.insert('', 'end', values=(
                row['Supplier'],
                f"{row['Delay Rate']:.1%}",
                f"{row['Avg Lead Time']:.2f}",
                f"{row['Avg Defect Rate']:.2f}"
            ))
    
    def update_products_table(self):
        """Update products table"""
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        for _, row in self.results['product_analysis'].iterrows():
            self.products_tree.insert('', 'end', values=(
                row['Product Type'],
                f"{row['Delay Rate']:.1%}",
                f"{row['Defect Rate']:.2f}",
                f"{row['Avg Shipping Time']:.1f}"
            ))
    
    def update_recommendations(self):
        """Update recommendations tab"""
        self.recommendations_text.delete(1.0, tk.END)
        
       
        self.recommendations_text.insert(tk.END, "🎯 KEY RECOMMENDATIONS\n", 'bold')
        self.recommendations_text.insert(tk.END, "="*50 + "\n\n")
        
        for i, rec in enumerate(self.results['report']['recommendations'], 1):
            self.recommendations_text.insert(tk.END, f"{i}. {rec}\n\n")
        
    
        self.recommendations_text.insert(tk.END, "\n📋 ACTION ITEMS\n", 'bold')
        self.recommendations_text.insert(tk.END, "="*50 + "\n\n")
        
        for b in self.results['bottlenecks'][:5]:
            self.recommendations_text.insert(tk.END, f"• {b['action']}\n")
    
    def enable_buttons(self):
        """Enable buttons after analysis"""
        self.run_btn.config(state='normal')
        self.view_dashboard_btn.config(state='normal')
        self.view_report_btn.config(state='normal')
        self.progress.stop()
    
    def view_dashboard(self):
        """Open dashboard in browser"""
        if self.results and self.results['dashboard']:
            dashboard_file = "supply_chain_bottleneck_dashboard.html"
            self.results['dashboard'].write_html(dashboard_file)
            webbrowser.open(dashboard_file)
            self.log_console(f"✅ Dashboard opened in browser: {dashboard_file}")
    
    def view_report(self):
        """Open JSON report"""
        import json
        report_file = "bottleneck_analysis_report.json"
        with open(report_file, 'w') as f:
            json.dump(self.results['report'], f, indent=2, default=str)
        
       
        import os
        os.startfile(report_file)
        self.log_console(f"✅ Report saved: {report_file}")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


class SupplyChainBottleneckSystem:
    """Main system integrating all components"""
    
    def __init__(self, csv_path):
        self.data_manager = SupplyChainDataManager(csv_path)
        self.preprocessor = DataPreprocessor()
        self.ai_engine = AIMLEngine()
        self.bottleneck_detector = BottleneckDetector()
        self.dashboard = SupplyChainDashboard()
        
    def run_complete_analysis(self):
        """Run complete supply chain bottleneck analysis"""
        print("\n" + "="*60)
        print("AI-Based Supply Chain Bottleneck Detection System")
        print("Using Kaggle Supply Chain Dataset")
        print("="*60)
        
        # Step 1: Load data
        print("\n[1/6] Loading dataset...")
        df = self.data_manager.load_dataset()
        self.data_manager.explore_data()
        
        # Step 2: Feature engineering
        print("\n[2/6] Engineering features...")
        df = self.data_manager.create_target_variable(df)
        df = self.data_manager.engineer_features(df)
        
        # Step 3: Preprocessing
        print("\n[3/6] Preprocessing data...")
        df_clean = self.preprocessor.clean_data(df)
        df_encoded = self.preprocessor.encode_categorical(df_clean)
        df_normalized, feature_cols = self.preprocessor.normalize_features(df_encoded)
        
        # Step 4: Prepare ML data
        print("\n[4/6] Training AI models...")
        X, y = self.preprocessor.prepare_ml_data(df_normalized)
        
      
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
    
        feature_importance = self.ai_engine.train_random_forest(X_train, y_train)
        self.ai_engine.train_anomaly_detection(X_train)
        
 
        y_pred = self.ai_engine.random_forest.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"✅ Model Accuracy: {accuracy:.2%}")
        print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
        
        # Step 5: Detect bottlenecks
        print("\n[5/6] Detecting bottlenecks...")
        bottlenecks = self.bottleneck_detector.detect_bottlenecks_by_category(
            df_normalized, feature_importance
        )
        
        print("\n🔍 Top Bottlenecks Detected:")
        for b in bottlenecks[:5]:
            print(f"  - {b['feature']}: {b['importance']:.2%} ({b['bottleneck_type']} - {b['severity']})")
            print(f"    Action: {b['action']}")
        
       
        supplier_performance = self.bottleneck_detector.analyze_supplier_performance(df_clean)
        product_analysis = self.bottleneck_detector.analyze_product_bottlenecks(df_clean)
        
        if supplier_performance is not None:
            print("\n🏭 Top Problematic Suppliers:")
            print(supplier_performance.head())
        
        if product_analysis is not None:
            print("\n📦 Top Problematic Product Types:")
            print(product_analysis.head())
        
        # Step 6: Create dashboard
        print("\n[6/6] Creating visualization dashboard...")
        dashboard_fig = self.dashboard.create_bottleneck_dashboard(
            bottlenecks, supplier_performance, product_analysis
        )
        
       
        report = {
            'dataset_info': {
                'total_records': len(df),
                'features': list(df.columns),
                'delay_rate': y.mean() * 100 if y is not None else 'N/A'
            },
            'model_performance': {
                'accuracy': accuracy,
                'feature_importance': feature_importance.head(10).to_dict('records')
            },
            'bottlenecks': bottlenecks[:10],
            'recommendations': [
                f"Focus on reducing {b['feature']} to improve supply chain efficiency"
                for b in bottlenecks[:5]
            ]
        }
        
        print("\n" + "="*60)
        print("✅ ANALYSIS COMPLETE!")
        print("="*60)
        
        return {
            'dashboard': dashboard_fig,
            'report': report,
            'bottlenecks': bottlenecks,
            'model_accuracy': accuracy,
            'supplier_performance': supplier_performance,
            'product_analysis': product_analysis
        }
class SupplyChainDataManager:
    """Manages the Kaggle supply chain dataset"""
    
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.raw_data = None
        self.processed_data = None
        
    def load_dataset(self):
        """Load the Kaggle supply chain dataset"""
        print("📂 Loading supply chain dataset...")
        self.raw_data = pd.read_csv(self.csv_path)
        print(f"✅ Loaded {len(self.raw_data)} records with {len(self.raw_data.columns)} columns")
        print(f"Columns: {list(self.raw_data.columns)}")
        return self.raw_data
    
    def explore_data(self):
        """Quick data exploration"""
        print("\n📊 Dataset Overview:")
        print(f"Shape: {self.raw_data.shape}")
        print(f"\nMissing Values:\n{self.raw_data.isnull().sum()}")
        print(f"\nData Types:\n{self.raw_data.dtypes}")
        print(f"\nSample Data:")
        print(self.raw_data.head())
        
    def create_target_variable(self, df):
        """Create delay flag based on shipping vs lead time"""
  
        if 'Shipping times' in df.columns and 'Lead time' in df.columns:
            df['delayed'] = (df['Shipping times'] > df['Lead time']).astype(int)
            df['delay_days'] = df['Shipping times'] - df['Lead time']
        else:
          
            df['delayed'] = np.random.choice([0, 1], size=len(df), p=[0.8, 0.2])
            df['delay_days'] = np.where(df['delayed'] == 1, 
                                       np.random.randint(1, 10, size=len(df)), 0)
        return df
    
    def engineer_features(self, df):
        """Create additional features for bottleneck detection"""
    
        if 'Revenue generated' in df.columns and 'Number of products sold' in df.columns:
            df['revenue_per_unit'] = df['Revenue generated'] / (df['Number of products sold'] + 1)
        
     
        if 'Manufacturing costs' in df.columns and 'Revenue generated' in df.columns:
            df['profit_margin'] = (df['Revenue generated'] - df['Manufacturing costs']) / df['Revenue generated']
        

        if 'Lead time' in df.columns and 'Manufacturing lead time' in df.columns:
            df['lead_time_ratio'] = df['Lead time'] / (df['Manufacturing lead time'] + 1)
        
      
        if 'Defect rates' in df.columns and 'Number of products sold' in df.columns:
            df['defect_impact'] = df['Defect rates'] * df['Number of products sold']
        
    
        if 'Stock levels' in df.columns and 'Number of products sold' in df.columns:
            df['stock_turnover'] = df['Number of products sold'] / (df['Stock levels'] + 1)
        
        return df
class DataPreprocessor:
    """Preprocess Kaggle supply chain dataset"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def clean_data(self, df):
        """Clean the dataset"""
     
        df = df.drop_duplicates()
        
      
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].median())
 
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df[col] = df[col].fillna('Unknown')
        
        return df
    
    def encode_categorical(self, df):
        """Encode categorical variables"""
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            le = LabelEncoder()
            df[col + '_encoded'] = le.fit_transform(df[col].astype(str))
            self.label_encoders[col] = le
            
        return df
    
    def normalize_features(self, df):
        """Normalize numerical features"""
      
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        exclude_cols = [col for col in numeric_cols if 'encoded' in col or col == 'delayed']
        feature_cols = [col for col in numeric_cols if col not in exclude_cols]
        
        if feature_cols:
            df[feature_cols] = self.scaler.fit_transform(df[feature_cols])
            
        return df, feature_cols
    
    def prepare_ml_data(self, df, target_col='delayed'):
        """Prepare data for machine learning"""
   
        if target_col in df.columns:
            y = df[target_col]
            X = df.drop(columns=[target_col])
        else:
            y = None
            X = df
        

        X_numeric = X.select_dtypes(include=[np.number])
        
        return X_numeric, y


class AIMLEngine:
    """AI/ML Engine for bottleneck detection"""
    
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.random_forest = None
        self.isolation_forest = None
        
    def train_random_forest(self, X_train, y_train):
        """Train Random Forest classifier"""
        self.random_forest = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.random_forest.fit(X_train, y_train)
        self.models['random_forest'] = self.random_forest
        
       
        importance_df = pd.DataFrame({
            'feature': X_train.columns,
            'importance': self.random_forest.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    def train_anomaly_detection(self, X_train):
        """Train Isolation Forest for anomaly detection"""
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        self.isolation_forest.fit(X_train)
        self.models['anomaly_detection'] = self.isolation_forest
        
    def predict_delays(self, X):
        """Predict delay probabilities"""
        if self.random_forest:
            probabilities = self.random_forest.predict_proba(X)
            predictions = self.random_forest.predict(X)
            return {
                'predictions': predictions,
                'probabilities': probabilities[:, 1],
                'risk_level': np.where(probabilities[:, 1] > 0.7, 'High',
                                     np.where(probabilities[:, 1] > 0.3, 'Medium', 'Low'))
            }
        return None
class BottleneckDetector:
    """Detect bottlenecks in supply chain"""
    
    def __init__(self):
        self.bottlenecks = []
        
    def detect_bottlenecks_by_category(self, df, feature_importance):
        """Identify bottlenecks based on feature importance"""
        bottlenecks = []
        
  
        top_features = feature_importance.head(10)
        
        for idx, row in top_features.iterrows():
            feature = row['feature']
            importance = row['importance']
            
          
            if 'Shipping' in feature or 'Lead' in feature:
                bottleneck_type = 'Logistics'
                severity = 'High' if importance > 0.15 else 'Medium'
            elif 'Defect' in feature:
                bottleneck_type = 'Quality'
                severity = 'High' if importance > 0.12 else 'Medium'
            elif 'Manufacturing' in feature:
                bottleneck_type = 'Production'
                severity = 'High' if importance > 0.12 else 'Medium'
            elif 'Stock' in feature or 'Inventory' in feature:
                bottleneck_type = 'Inventory'
                severity = 'Medium'
            else:
                bottleneck_type = 'Other'
                severity = 'Low'
            
            bottlenecks.append({
                'feature': feature,
                'importance': importance,
                'bottleneck_type': bottleneck_type,
                'severity': severity,
                'action': self.get_action_recommendation(bottleneck_type, feature)
            })
        
        return bottlenecks
    
    def get_action_recommendation(self, bottleneck_type, feature):
        """Get actionable recommendation"""
        recommendations = {
            'Logistics': f'Optimize {feature} - consider alternative carriers or routes',
            'Quality': f'Address {feature} - implement quality control measures',
            'Production': f'Improve {feature} - optimize manufacturing process',
            'Inventory': f'Review {feature} - adjust stock levels and reorder points'
        }
        return recommendations.get(bottleneck_type, 'Monitor and analyze further')
    
    def analyze_supplier_performance(self, df):
        """Analyze bottlenecks by supplier"""
        if 'Supplier name' in df.columns and 'delayed' in df.columns:
            supplier_performance = df.groupby('Supplier name').agg({
                'delayed': 'mean',
                'Lead time': 'mean',
                'Defect rates': 'mean',
                'Revenue generated': 'sum'
            }).reset_index()
            
            supplier_performance.columns = ['Supplier', 'Delay Rate', 'Avg Lead Time', 
                                           'Avg Defect Rate', 'Total Revenue']
            supplier_performance = supplier_performance.sort_values('Delay Rate', ascending=False)
            
            return supplier_performance
        return None
    
    def analyze_product_bottlenecks(self, df):
        """Analyze bottlenecks by product type"""
        if 'Product type' in df.columns and 'delayed' in df.columns:
            product_analysis = df.groupby('Product type').agg({
                'delayed': 'mean',
                'Defect rates': 'mean',
                'Shipping times': 'mean',
                'Number of products sold': 'sum'
            }).reset_index()
            
            product_analysis.columns = ['Product Type', 'Delay Rate', 'Defect Rate', 
                                       'Avg Shipping Time', 'Units Sold']
            return product_analysis.sort_values('Delay Rate', ascending=False)
        return None
class SupplyChainDashboard:
    """Interactive dashboard for visualization"""
    
    def create_bottleneck_dashboard(self, bottlenecks, supplier_performance, product_analysis):
        """Create comprehensive dashboard for bottleneck visualization"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Top Bottleneck Factors', 'Supplier Delay Rates',
                           'Product Type Performance', 'Bottleneck Severity Distribution'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'pie'}]],
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        

        if bottlenecks:
            top_bottlenecks = bottlenecks[:10]
            fig.add_trace(
                go.Bar(x=[b['feature'][:25] for b in top_bottlenecks],
                      y=[b['importance'] for b in top_bottlenecks],
                      marker_color='red',
                      name='Importance',
                      text=[f"{b['importance']:.1%}" for b in top_bottlenecks],
                      textposition='outside'),
                row=1, col=1
            )
            fig.update_xaxes(tickangle=45, row=1, col=1)
            fig.update_yaxes(title_text="Importance Score", row=1, col=1)
        
      
        if supplier_performance is not None and len(supplier_performance) > 0:
            top_suppliers = supplier_performance.head(10)
            fig.add_trace(
                go.Bar(x=top_suppliers['Supplier'],
                      y=top_suppliers['Delay Rate'] * 100,
                      marker_color='orange',
                      name='Delay Rate %',
                      text=[f"{x:.1f}%" for x in top_suppliers['Delay Rate'] * 100],
                      textposition='outside'),
                row=1, col=2
            )
            fig.update_xaxes(tickangle=45, row=1, col=2)
            fig.update_yaxes(title_text="Delay Rate (%)", row=1, col=2)
        

        if product_analysis is not None and len(product_analysis) > 0:
            top_products = product_analysis.head(10)
            fig.add_trace(
                go.Bar(x=top_products['Product Type'],
                      y=top_products['Delay Rate'] * 100,
                      marker_color='lightblue',
                      name='Delay Rate %',
                      text=[f"{x:.1f}%" for x in top_products['Delay Rate'] * 100],
                      textposition='outside'),
                row=2, col=1
            )
            fig.update_xaxes(tickangle=45, row=2, col=1)
            fig.update_yaxes(title_text="Delay Rate (%)", row=2, col=1)
        
      
        if bottlenecks:
            severity_counts = pd.DataFrame(bottlenecks)['severity'].value_counts()
            fig.add_trace(
                go.Pie(labels=severity_counts.index,
                      values=severity_counts.values,
                      name='Severity',
                      hole=0.3,
                      marker=dict(colors=['red', 'orange', 'yellow'])),
                row=2, col=2
            )
        
     
        fig.update_layout(
            height=800,
            title_text="Supply Chain Bottleneck Detection Dashboard",
            title_font_size=20,
            showlegend=True,
            template='plotly_white'
        )
        
        return fig
    
    def create_enhanced_dashboard(self, bottlenecks, supplier_performance, product_analysis, df, predictions):
        """Create enhanced dashboard with more visualizations"""
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('Top Bottleneck Factors', 'Supplier Delay Rates',
                           'Product Type Performance', 'Bottleneck Severity Distribution',
                           'Delay Prediction Distribution', 'Feature Correlation Heatmap'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'pie'}],
                   [{'type': 'histogram'}, {'type': 'heatmap'}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Top bottleneck factors
        if bottlenecks:
            top_bottlenecks = bottlenecks[:10]
            fig.add_trace(
                go.Bar(x=[b['feature'][:25] for b in top_bottlenecks],
                      y=[b['importance'] for b in top_bottlenecks],
                      marker_color='red',
                      name='Importance',
                      text=[f"{b['importance']:.1%}" for b in top_bottlenecks],
                      textposition='outside'),
                row=1, col=1
            )
        
    
        if supplier_performance is not None:
            top_suppliers = supplier_performance.head(10)
            fig.add_trace(
                go.Bar(x=top_suppliers['Supplier'],
                      y=top_suppliers['Delay Rate'] * 100,
                      marker_color='orange',
                      name='Delay Rate %',
                      text=[f"{x:.1f}%" for x in top_suppliers['Delay Rate'] * 100],
                      textposition='outside'),
                row=1, col=2
            )
        

        if product_analysis is not None:
            top_products = product_analysis.head(10)
            fig.add_trace(
                go.Bar(x=top_products['Product Type'],
                      y=top_products['Delay Rate'] * 100,
                      marker_color='lightblue',
                      name='Delay Rate %',
                      text=[f"{x:.1f}%" for x in top_products['Delay Rate'] * 100],
                      textposition='outside'),
                row=2, col=1
            )
        

        if bottlenecks:
            severity_counts = pd.DataFrame(bottlenecks)['severity'].value_counts()
            fig.add_trace(
                go.Pie(labels=severity_counts.index,
                      values=severity_counts.values,
                      name='Severity',
                      hole=0.3,
                      marker=dict(colors=['red', 'orange', 'yellow'])),
                row=2, col=2
            )
        
    
        if predictions and 'probabilities' in predictions:
            fig.add_trace(
                go.Histogram(x=predictions['probabilities'],
                            nbinsx=20,
                            marker_color='green',
                            name='Delay Probability'),
                row=3, col=1
            )
            fig.update_xaxes(title_text="Delay Probability", row=3, col=1)
            fig.update_yaxes(title_text="Frequency", row=3, col=1)
        
  
        if df is not None:
            numeric_df = df.select_dtypes(include=[np.number])
            if len(numeric_df.columns) > 1:
                corr_matrix = numeric_df.corr().head(10)
                fig.add_trace(
                    go.Heatmap(z=corr_matrix.values,
                              x=corr_matrix.columns,
                              y=corr_matrix.columns,
                              colorscale='RdBu',
                              zmin=-1, zmax=1),
                    row=3, col=2
                )
        
        fig.update_layout(
            height=1200,
            title_text="Supply Chain Bottleneck Detection Dashboard",
            title_font_size=20,
            showlegend=True,
            template='plotly_white'
        )
        
  
        fig.update_xaxes(tickangle=45, row=1, col=1)
        fig.update_xaxes(tickangle=45, row=1, col=2)
        fig.update_xaxes(tickangle=45, row=2, col=1)
        
        return fig

if __name__ == "__main__":
  
    app = SupplyChainGUI()
    app.run()
  