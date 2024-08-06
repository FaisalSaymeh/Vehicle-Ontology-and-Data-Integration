from flask import Flask, request, jsonify
import rdflib
import logging

# Initialize Flask application
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize RDF graph and load the TTL file
g = rdflib.Graph()
g.parse("d:/Master/Semantic Technologies/Project/2/merged_ontology_with_data.ttl", format="turtle")

# Query the the ontology (SPARQL)

# 1:
@app.route('/vehicle_brands', methods=['GET'])
def vehicle_brands():
    query = """
    PREFIX ex: <http://example.org/vehicle/>
    SELECT ?vehicle ?brand
    WHERE {
        ?vehicle a ex:Vehicle ;
                 ex:brand ?brand .
    }
    LIMIT 10
    """
    results = g.query(query)
    output = [{"vehicle": str(row.vehicle), "brand": str(row.brand)} for row in results]
    return jsonify(output)

# 2:    
@app.route('/models_prices', methods=['GET'])
def models_prices():
    query = """
    PREFIX ex: <http://example.org/vehicle/>
    SELECT ?model ?price
    WHERE {
        ?vehicle ex:model ?model ;
                 ex:price ?price .
    }
    LIMIT 10
    """
    results = g.query(query)
    output = [{"model": str(row.model), "price": str(row.price)} for row in results]
    return jsonify(output)

# 3:
@app.route('/vehicle_hp', methods=['GET'])
def vehicle_hp():
    query = """
    PREFIX ex: <http://example.org/vehicle/>
    SELECT ?model ?hp
    WHERE {
        ?vehicle ex:model ?model ;
                 ex:engineHP ?hp .
    }
    LIMIT 10
    """
    results = g.query(query)
    output = [{"model": str(row.model), "horsepower": str(row.hp)} for row in results]
    return jsonify(output)

# 4:
@app.route('/vehicles_sorted_by_price', methods=['GET'])
def vehicles_sorted_by_price():
    query = """
    PREFIX ex: <http://example.org/vehicle/>
    SELECT ?vehicle ?price
    WHERE {
        ?vehicle ex:price ?price .
    }
    ORDER BY ?price
    LIMIT 10
    """
    results = g.query(query)
    output = [{"vehicle": str(row.vehicle), "price": str(row.price)} for row in results]
    return jsonify(output)

# 5:
@app.route('/vehicles_by_years', methods=['GET'])
def vehicles_by_years():
    query = """
    PREFIX ex: <http://example.org/vehicle/>
    SELECT ?vehicle
    WHERE {
        ?vehicle ex:year ?year .
        FILTER(?year >= 2005 && ?year <= 2010)
    }
    LIMIT 5
    """
    results = g.query(query)
    output = [{"vehicle": str(row.vehicle)} for row in results]
    return jsonify(output)

# 6:
@app.route('/average_price_by_brand', methods=['GET'])
def average_price_by_brand():
    query = """
    PREFIX ex: <http://example.org/vehicle/>
    SELECT ?brand (AVG(?price) as ?avgPrice)
    WHERE {
        ?vehicle ex:brand ?brand ;
                 ex:price ?price .
    }
    GROUP BY ?brand
    LIMIT 10
    """
    results = g.query(query)
    output = [{"brand": str(row.brand), "average_price": str(row.avgPrice)} for row in results]
    return jsonify(output)

# 7:
@app.route('/vehicle_optional_equipment', methods=['GET'])
def vehicle_optional_equipment():
    query = """
    PREFIX ex: <http://example.org/vehicle/>
    SELECT ?vehicle ?equipment ?price
    WHERE {
        ?vehicle ex:price ?price .
        OPTIONAL { ?vehicle ex:hasEquipment ?equipment . }
    }
    LIMIT 5
    """
    results = g.query(query)
    output = [{"vehicle": str(row.vehicle), 
               "equipment": str(row.equipment) if row.equipment else 'No equipment',
               "price": str(row.price)} for row in results]
    return jsonify(output)

# 8:
@app.route('/vehicle_warranty_service', methods=['GET'])
def vehicle_warranty_service():
    query = """
    PREFIX ex: <http://example.org/vehicle/>
    SELECT ?vehicle ?warrantyPeriod ?lastServiceDate
    WHERE {
        ?vehicle ex:model ?model .
        OPTIONAL {
            ?vehicle ex:warrantyPeriod ?warrantyPeriod .
            OPTIONAL { ?vehicle ex:lastServiceDate ?lastServiceDate . }
        }
    }
    LIMIT 5
    """
    results = g.query(query)
    output = [{"vehicle": str(row.vehicle), 
               "warranty_period": str(row.warrantyPeriod) if row.warrantyPeriod else 'No warranty info',
               "last_service_date": str(row.lastServiceDate) if row.lastServiceDate else 'No service info'} for row in results]
    return jsonify(output)

# 9:
@app.route('/vehicle_basic_info', methods=['GET'])
def vehicle_basic_info():
    query = """
    PREFIX ex: <http://example.org/vehicle/>
    SELECT ?vehicle ?brand ?model ?year ?price
    WHERE {
        ?vehicle ex:brand ?brand ;
                 ex:model ?model ;
                 ex:year ?year ;
                 ex:price ?price .
    }
    LIMIT 10
    """
    results = g.query(query)
    output = [{"vehicle": str(row.vehicle), 
               "brand": str(row.brand), 
               "model": str(row.model), 
               "year": str(row.year), 
               "price": str(row.price)} for row in results]
    return jsonify(output)

# 10:
@app.route('/vehicles_by_year_and_price', methods=['GET'])
def vehicles_by_year_and_price():
    query = """
    PREFIX ex: <http://example.org/vehicle/>
    SELECT ?vehicle ?brand ?model ?year ?price
    WHERE {
        ?vehicle ex:brand ?brand ;
                 ex:model ?model ;
                 ex:year ?year ;
                 ex:price ?price .
        FILTER(?year > 2015 && ?price > 50000)
    }
    LIMIT 10
    """
    results = g.query(query)
    output = [{"vehicle": str(row.vehicle), 
               "brand": str(row.brand), 
               "model": str(row.model), 
               "year": str(row.year), 
               "price": str(row.price)} for row in results]
    return jsonify(output)
    
#  Running the Application
if __name__ == '__main__':
    app.run(debug=True, port=5000)

