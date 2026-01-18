# common/callbacks.py
from langchain_core.callbacks import BaseCallbackHandler
from sqlalchemy.orm import Session
from database.rdm import RunTrace
from datetime import datetime
import uuid

class DBLoggingCallbackHandler(BaseCallbackHandler):
    def __init__(self, session_id: str, db: Session):
        self.session_id = session_id
        self.db = db
        self.run_map = {} # 실행 중인 작업의 ID를 추적하기 위함

    # 1. 도구 실행 시작 시
    def on_tool_start(self, serialized: dict, input_str: str, **kwargs):
        run_id = kwargs.get("run_id", str(uuid.uuid4()))
        name = serialized.get("name", "unknown_tool")
        
        # DB에 '시작' 상태로 기록
        trace = RunTrace(
            id=run_id,
            session_id=self.session_id,
            type="tool",
            name=name,
            inputs={"input": input_str},
            status="started",
            start_time=datetime.now()
        )
        self.db.add(trace)
        self.db.commit()
        self.run_map[run_id] = trace # 메모리에 잠시 저장

    # 2. 도구 실행 완료 시
    def on_tool_end(self, output: str, **kwargs):
        run_id = kwargs.get("run_id")
        trace = self.run_map.get(run_id)
        
        if trace:
            trace.outputs = {"output": output}
            trace.status = "success"
            trace.end_time = datetime.now()
            trace.duration = (trace.end_time - trace.start_time).total_seconds()
            
            self.db.add(trace) # Update
            self.db.commit()

    # 3. 도구 에러 발생 시
    def on_tool_error(self, error: BaseException, **kwargs):
        run_id = kwargs.get("run_id")
        trace = self.run_map.get(run_id)
        
        if trace:
            trace.error_message = str(error)
            trace.status = "error"
            trace.end_time = datetime.now()
            
            self.db.add(trace)
            self.db.commit()