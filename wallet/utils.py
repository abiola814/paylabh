from billPayment.bills import walletProcess
from user.models import User
from wallet.serializer import TransactionSerializer
from wallet.models import Transaction
import uuid

def labtransfer(request,amount,labName,id):
    if not walletProcess(amount=amount,user=request.user,id=id,type=1):
        return "insufficient balance","failed"
    if not walletProcess(amount=amount,user=request.user,type=2,id=id):
        return "unable to debit wallet","failed"

    taguser= labName.replace('LabTag')
    user= User.objects.get(tag=taguser)
    if walletProcess(amount=amount,user=user,type=3,id=id):
        balance = walletProcess(amount=amount,user=user)
        trans = Transaction,object.create(user=user,name=f"{user.last_name} {user.first_name}",
    transaction_type="Credit",transaction_id= (uuid.uuid4())[:12],reference_id= (uuid.uuid4())[:12],status="success",
    description=f"transfer from  {request.user.last_name}",remainbalance=balance,amount=amount)
        return "money sent","success"
    else:
        return "unable to credit other account contact the customer care"

    
    


