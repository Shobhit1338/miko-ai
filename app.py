from flask import Flask, request
import pymysql

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_program():
    program = request.get_data().decode('utf-8')

    # Connect to MySQL database
    connection = pymysql.connect(host='Shobhit',
                                 port=5000,
                                 user='root',
                                 password='qwerty123',
                                 db='myDB')
    cursor = connection.cursor()

    # Save the program in the database
    cursor.execute("INSERT INTO programs (program) VALUES (%s)", (program,))
    program_id = cursor.lastrowid

    # Initialize registers
    registers = {'REG1': 0, 'REG2': 0}

    # Split the program into instructions
    instructions = program.split('\n')

    # Execute each instruction
    for instruction in instructions:
        if instruction.startswith('MV'):
            parts = instruction.split()
            register = parts[1]
            value = int(parts[2].lstrip('#'))
            registers[register] = value
        elif instruction.startswith('ADD'):
            parts = instruction.split()
            register1 = parts[1]
            if parts[2].startswith('#'):
                constant = int(parts[2].lstrip('#'))
                registers[register1] += constant
            else:
                register2 = parts[2]
                registers[register1] += registers[register2]
        elif instruction.startswith('SHOW'):
            parts = instruction.split()
            register = parts[1]
            print(f"{register}: {registers[register]}")

    # Save the final result in the database
    cursor.execute("UPDATE programs SET result = %s WHERE id = %s", (registers['REG1'], program_id))
    connection.commit()

    # Close the database connection
    cursor.close()
    connection.close()

    return 'Program executed successfully.'




if __name__ == '__main__':
    app.run()
