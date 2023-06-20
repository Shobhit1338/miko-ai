from flask import Flask, request
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="qwerty123",
    database="db123"
)
cursor = db.cursor()

# Create a table to store program execution details
cursor.execute("CREATE TABLE IF NOT EXISTS program_execution (id INT AUTO_INCREMENT PRIMARY KEY, program TEXT, status VARCHAR(10))")
db.commit()

@app.route('/', methods=['POST'])
def execute_program():
    program = request.form['program']
    registers = {}  # Dictionary to store register values
    lines = program.split('\n')  # Split program into lines

    for line in lines:
        line = line.strip()  # Remove leading/trailing spaces
        parts = line.split()

        if line.startswith('MV'):
            if len(parts) != 3:
                save_execution_status(program, 'failure')
                return "Invalid number of arguments for MV instruction"
            _, register, value = parts
            try:
                registers[register] = int(value.lstrip('#'))
            except ValueError:
                save_execution_status(program, 'failure')
                return f"Invalid value for register {register}: {value}"
        elif line.startswith('ADD'):
            if len(parts) != 3:
                save_execution_status(program, 'failure')
                return "Invalid number of arguments for ADD instruction"
            _, reg1, reg2_or_constant = parts
            if reg2_or_constant.startswith('REG'):
                register = reg2_or_constant.strip(',')
                registers[reg1] += registers[register]
            elif reg2_or_constant.startswith('#'):
                constant = int(reg2_or_constant.lstrip('#').strip(','))
                registers[reg1] += constant
        elif line.startswith('SHOW'):
            _, register = line.split()
            result = registers.get(register, 0)
            save_execution_status(program, 'success')
            return str(result)

    save_execution_status(program, 'failure')
    return "Program executed successfully."


def save_execution_status(program, status):
    sql = "INSERT INTO program_execution (program, status) VALUES (%s, %s)"
    values = (program, status)
    cursor.execute(sql, values)
    db.commit()

if __name__ == '__main__':
    app.run()
