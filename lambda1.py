import json
import boto3
from datetime import datetime
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Supply Chain Risk Analyzer for Bedrock Agent Action Group
    """
    
    logger.info(f"Received event: {json.dumps(event)}")
    print("Event")
    print(event)
    
    try:
        # Parse the agent request
        # agent_request_body = json.loads(event.get('body', '{}'))
        agent_request_body = event
        print(agent_request_body)
        action_group = agent_request_body.get('actionGroup', '')
        function_name = agent_request_body.get('function', '')
        parameters = agent_request_body.get('parameters', [])
        
        logger.info(f"Action Group: {action_group}, Function: {function_name}")
        
        # Convert parameters list to dictionary
        params = {}
        for param in parameters:
            params[param['name']] = param['value']
        print("Paramas")
        print(params)
        # Route to appropriate function
        if function_name == 'analyze_supplier_risk':
            result = analyze_supplier_risk(params)
        elif function_name == 'find_alternative_suppliers':
            result = find_alternative_suppliers(params)
        elif function_name == 'calculate_crisis_impact':
            result = calculate_crisis_impact(params)
        elif function_name == 'generate_procurement_recommendations':
            result = generate_procurement_recommendations(params)
        else:
            result = {
                'error': f'Unknown function: {function_name}'
            }
        
        # Format response for Bedrock Agent
        response = {
            'messageVersion': '1.0',
            'response': {
                'actionGroup': action_group,
                'function': function_name,
                'functionResponse': {
                    'responseBody': {
                        'TEXT': {
                            'body': json.dumps(result)
                        }
                    }
                }
            }
        }
        
        logger.info(f"Response: {json.dumps(response)}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        
        error_response = {
            'messageVersion': '1.0',
            'response': {
                'actionGroup': event.get('actionGroup', ''),
                'function': event.get('function', ''),
                'functionResponse': {
                    'responseBody': {
                        'TEXT': {
                            'body': json.dumps({
                                'error': str(e),
                                'message': 'Lambda function encountered an error'
                            })
                        }
                    }
                }
            }
        }
        
        return error_response

def analyze_supplier_risk(params):
    """Analyze risk level for a specific supplier"""
    
    supplier_name = params.get('supplier_name', 'Unknown')
    location = params.get('location', 'Unknown')
    
    # Mock supplier risk database (in real implementation, this would query DynamoDB)
    supplier_risks = {
        'TSMC': {'risk_score': 85, 'reason': 'High geographic concentration in Taiwan, earthquake risk'},
        'Samsung': {'risk_score': 45, 'reason': 'Diversified locations, stable operations'},
        'Foxconn': {'risk_score': 60, 'reason': 'China dependency, labor issues'},
        'Intel': {'risk_score': 25, 'reason': 'US-based, multiple facilities'},
        'SK Hynix': {'risk_score': 50, 'reason': 'South Korea concentration'},
        'Micron': {'risk_score': 30, 'reason': 'Multiple global locations'}
    }
    
    # Calculate risk based on location
    location_risks = {
        'Taiwan': 85,
        'China': 70,
        'South Korea': 45,
        'Japan': 35,
        'USA': 20,
        'Europe': 25
    }
    
    base_risk = supplier_risks.get(supplier_name, {'risk_score': 50, 'reason': 'Unknown supplier'})
    location_risk = location_risks.get(location, 50)
    
    # Combine supplier and location risk
    final_risk = min(100, (base_risk['risk_score'] + location_risk) // 2)
    
    return {
        'supplier_name': supplier_name,
        'location': location,
        'risk_score': final_risk,
        'risk_level': 'High' if final_risk > 70 else 'Medium' if final_risk > 40 else 'Low',
        'risk_factors': base_risk['reason'],
        'timestamp': datetime.now().isoformat()
    }

def find_alternative_suppliers(params):
    """Find alternative suppliers for a component"""
    
    component = params.get('component', 'Unknown')
    affected_supplier = params.get('affected_supplier', 'Unknown')
    
    # Mock alternative supplier database
    alternatives = {
        'semiconductors': [
            {'name': 'Intel', 'location': 'USA', 'capacity': 'High', 'lead_time': '12-16 weeks'},
            {'name': 'Samsung', 'location': 'South Korea', 'capacity': 'High', 'lead_time': '10-14 weeks'},
            {'name': 'GlobalFoundries', 'location': 'USA/Europe', 'capacity': 'Medium', 'lead_time': '14-18 weeks'}
        ],
        'memory': [
            {'name': 'Samsung', 'location': 'South Korea', 'capacity': 'High', 'lead_time': '8-12 weeks'},
            {'name': 'Micron', 'location': 'USA', 'capacity': 'High', 'lead_time': '10-14 weeks'},
            {'name': 'SK Hynix', 'location': 'South Korea', 'capacity': 'Medium', 'lead_time': '10-16 weeks'}
        ],
        'assembly': [
            {'name': 'Pegatron', 'location': 'Taiwan/China', 'capacity': 'High', 'lead_time': '6-10 weeks'},
            {'name': 'Wistron', 'location': 'Taiwan/India', 'capacity': 'Medium', 'lead_time': '8-12 weeks'},
            {'name': 'Flextronics', 'location': 'Global', 'capacity': 'High', 'lead_time': '6-10 weeks'}
        ]
    }
    
    component_alternatives = alternatives.get(component.lower(), [])
    
    # Filter out the affected supplier
    filtered_alternatives = [
        alt for alt in component_alternatives 
        if alt['name'].lower() != affected_supplier.lower()
    ]
    
    return {
        'component': component,
        'affected_supplier': affected_supplier,
        'alternatives': filtered_alternatives,
        'recommendation': filtered_alternatives[0] if filtered_alternatives else None,
        'total_options': len(filtered_alternatives),
        'timestamp': datetime.now().isoformat()
    }

def calculate_crisis_impact(params):
    """Calculate impact of a supply chain crisis"""
    
    crisis_type = params.get('crisis_type', 'Unknown')
    affected_region = params.get('affected_region', 'Unknown')
    severity = params.get('severity', 'Medium')
    
    # Mock impact calculation
    impact_multipliers = {
        'earthquake': 1.5,
        'flood': 1.2,
        'strike': 1.3,
        'port_closure': 1.4,
        'geopolitical': 1.6
    }
    
    regional_impacts = {
        'Taiwan': {'semiconductor_impact': 85, 'assembly_impact': 60},
        'China': {'semiconductor_impact': 40, 'assembly_impact': 80},
        'South Korea': {'semiconductor_impact': 70, 'memory_impact': 85},
        'Japan': {'component_impact': 60, 'material_impact': 70}
    }
    
    base_impact = regional_impacts.get(affected_region, {'general_impact': 50})
    multiplier = impact_multipliers.get(crisis_type.lower(), 1.0)
    
    severity_multiplier = {'Low': 0.7, 'Medium': 1.0, 'High': 1.5}.get(severity, 1.0)
    
    # Calculate various impacts
    production_delay_days = int(10 * multiplier * severity_multiplier)
    cost_increase_percent = int(15 * multiplier * severity_multiplier)
    revenue_at_risk_percent = int(25 * multiplier * severity_multiplier)
    
    return {
        'crisis_type': crisis_type,
        'affected_region': affected_region,
        'severity': severity,
        'impact_assessment': {
            'production_delay_days': production_delay_days,
            'cost_increase_percent': cost_increase_percent,
            'revenue_at_risk_percent': revenue_at_risk_percent,
            'recovery_time_weeks': production_delay_days // 7 + 2
        },
        'affected_components': list(base_impact.keys()),
        'timestamp': datetime.now().isoformat()
    }

def generate_procurement_recommendations(params):
    """Generate procurement recommendations based on crisis"""
    
    crisis_type = params.get('crisis_type', 'Unknown')
    affected_suppliers = params.get('affected_suppliers', '').split(',')
    urgency = params.get('urgency', 'Medium')
    
    recommendations = []
    
    # Generate recommendations based on affected suppliers
    for supplier in affected_suppliers:
        supplier = supplier.strip()
        if supplier:
            if 'TSMC' in supplier or 'Taiwan' in supplier:
                recommendations.extend([
                    {
                        'action': 'immediate_alternative_sourcing',
                        'supplier': 'Samsung',
                        'component': 'Semiconductors',
                        'quantity': 'Increase order by 40%',
                        'timeline': '2-3 weeks',
                        'priority': 'Critical'
                    },
                    {
                        'action': 'inventory_buffer_increase',
                        'component': 'Memory chips',
                        'increase_percent': 60,
                        'timeline': '1 week',
                        'priority': 'High'
                    }
                ])
            
            if 'Foxconn' in supplier or 'assembly' in supplier.lower():
                recommendations.append({
                    'action': 'diversify_assembly',
                    'supplier': 'Pegatron',
                    'component': 'Assembly services',
                    'timeline': '3-4 weeks',
                    'priority': 'Medium'
                })
    
    # Add general recommendations
    recommendations.extend([
        {
            'action': 'activate_emergency_procurement',
            'description': 'Activate pre-approved emergency supplier contracts',
            'timeline': 'Immediate',
            'priority': 'Critical'
        },
        {
            'action': 'expedite_shipping',
            'description': 'Switch to air freight for critical components',
            'cost_impact': '+25% shipping costs',
            'timeline': '1-2 days',
            'priority': 'High'
        }
    ])
    
    return {
        'crisis_type': crisis_type,
        'affected_suppliers': affected_suppliers,
        'urgency': urgency,
        'recommendations': recommendations,
        'total_actions': len(recommendations),
        'estimated_cost_impact': '$2.5M - $5.2M',
        'estimated_time_savings': '3-6 weeks',
        'timestamp': datetime.now().isoformat()
    }