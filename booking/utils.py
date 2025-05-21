# дополнительные функции
def get_seats_matrix(session):
    seats = session.seats.order_by('row', 'number')
    matrix = []
    current_row = []

    for seat in seats:
        if seat.row != len(matrix) + 1:
            if current_row:
                matrix.append(current_row)
            current_row = []
        current_row.append({
            'id': seat.id,
            'number': seat.number,
            'reserved': seat.is_reserved
        })

    return matrix