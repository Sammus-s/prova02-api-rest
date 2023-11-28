import random

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import select

from src.config.database import get_session
from src.models.reservas_model import Reserva
from src.models.voos_model import Voo

reservas_router = APIRouter(prefix="/reservas")


@reservas_router.get("/{id_voo}")
def lista_reservas_voo(id_voo: int):
    with get_session() as session:
        statement = select(Reserva).where(Reserva.voo_id == id_voo)
        reservas = session.exec(statement).all()
        return reservas


@reservas_router.post("")
def cria_reserva(reserva: Reserva):
    with get_session() as session:
        voo = session.exec(select(Voo).where(Voo.id == reserva.voo_id)).first()

        if not voo:
            return JSONResponse(
                content={"message": f"Voo com id {reserva.voo_id} não encontrado."},
                status_code=404,
            )

        #Valida se já existe uma reserva para o documento        
        if session.exec(select(Reserva).where(Reserva.documento == reserva.documento)).first():
            return JSONResponse(
                content={"message": f"já existe uma reserva com o documento {reserva.documento}."},
                status_code=404,
            )

        codigo_reserva = "".join(
            [str(random.randint(0, 999)).zfill(3) for _ in range(2)]
        )

        reserva.codigo_reserva = codigo_reserva
        session.add(reserva)
        session.commit()
        session.refresh(reserva)
        return reserva


@reservas_router.post("/{codigo_reserva}/checkin/{num_poltrona}")
def faz_checkin(codigo_reserva: str, num_poltrona: int):
    with get_session() as session:
        reserva = session.exec(select(Reserva).where(Reserva.codigo_reserva == codigo_reserva)).first()

        if not reserva:
            return JSONResponse(
                content={"message": "Reserva não encontrada."},
                status_code=404
            )
        
        voo = session.exec(select(Voo).where(Voo.id == reserva.voo_id)).first()                

        print(voo.id)
        print(voo.poltrona_1)

        if num_poltrona == 1 and not voo.poltrona_1:
            voo.poltrona_1 = codigo_reserva
        elif num_poltrona == 2 and not voo.poltrona_2:
            voo.poltrona_2 = codigo_reserva
        elif num_poltrona == 3 and not voo.poltrona_3:
            voo.poltrona_3 = codigo_reserva
        elif num_poltrona == 4 and not voo.poltrona_4:
            voo.poltrona_4 = codigo_reserva
        elif num_poltrona == 5 and not voo.poltrona_5:
            voo.poltrona_5 = codigo_reserva
        elif num_poltrona == 6 and not voo.poltrona_6:
            voo.poltrona_6 = codigo_reserva
        elif num_poltrona == 7 and not voo.poltrona_7:
            voo.poltrona_7 = codigo_reserva
        elif num_poltrona == 8 and not voo.poltrona_8:
            voo.poltrona_8 = codigo_reserva
        elif num_poltrona == 9 and not voo.poltrona_9:
            voo.poltrona_9 = codigo_reserva
        else:
            return JSONResponse(
                content={"message": "poltrona já está ocupada ou código inválido"},
                status_code=404
            )        

        session.add(voo)
        session.commit()
        session.refresh(voo)
        return voo
        

# TODO - Implementar troca de reserva de poltrona
